from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
import models, schemas
from database import get_db
from fastapi.responses import StreamingResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import io

router = APIRouter()

class ReportePaciente(BaseModel):
    paciente: Optional[schemas.Paciente] = None
    citas: List[schemas.Cita] = []
    progresos: List[schemas.Progreso] = []
    mediciones: List[schemas.MedicionAntropometrica] = []
    composiciones: List[schemas.ComposicionCorporal] = []
    metricas: dict = {}

@router.get("/paciente/{id_paciente}", response_model=ReportePaciente)
def get_reporte_paciente(
    id_paciente: int,
    desde_fecha: Optional[datetime] = Query(None),
    hasta_fecha: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    print(f"DEBUG: Reporte para paciente {id_paciente} - Inicio")

    # Buscar paciente
    paciente = db.query(models.Paciente).filter(models.Paciente.id_paciente == id_paciente).first()
    if not paciente:
        print(f"DEBUG: Paciente {id_paciente} no encontrado")
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    print(f"DEBUG: Paciente: {paciente.nombre}")

    # Query citas con joinedload
    query_citas = db.query(models.Cita).filter(models.Cita.id_paciente == id_paciente).options(
        joinedload(models.Cita.progresos),
        joinedload(models.Cita.mediciones)
    )
    if desde_fecha is not None:  # Fix: Chequea is not None para evitar Query object
        query_citas = query_citas.filter(models.Cita.fecha >= desde_fecha)
        print(f"DEBUG: Filtro desde: {desde_fecha}")
    if hasta_fecha is not None:  # Fix: Igual para hasta
        query_citas = query_citas.filter(models.Cita.fecha <= hasta_fecha)
        print(f"DEBUG: Filtro hasta: {hasta_fecha}")
    citas = query_citas.order_by(models.Cita.fecha.desc()).all()
    print(f"DEBUG: Citas: {len(citas)}")

    # Progresos y mediciones
    progresos = []
    mediciones = []
    for c in citas:
        progresos.extend(c.progresos)
        mediciones.extend(c.mediciones)
    print(f"DEBUG: Progresos: {len(progresos)}, Mediciones: {len(mediciones)}")

    # Composiciones
    composiciones = []
    for c in citas:
        comp = db.query(models.ComposicionCorporal).filter(models.ComposicionCorporal.id_cita == c.id_cita).first()
        if comp:
            if comp.masa_grasa and c.peso:
                comp.porcentaje_grasa = round((comp.masa_grasa / float(c.peso)) * 100, 2)
            composiciones.append(comp)
    print(f"DEBUG: Composiciones: {len(composiciones)}")

    # Métricas
    imcs = [float(c.imc or 0) for c in citas if c.imc]
    pesos = [float(c.peso or 0) for c in citas if c.peso]
    metricas = {
        "imc_promedio": round(sum(imcs) / len(imcs), 2) if imcs else 0,
        "peso_inicial": pesos[-1] if pesos else 0,
        "peso_final": pesos[0] if pesos else 0,
        "tendencia_peso_kg": round(pesos[0] - pesos[-1], 2) if len(pesos) > 1 else 0,
        "total_citas": len(citas)
    }
    print(f"DEBUG: Métricas: {metricas}")

    print("DEBUG: Reporte listo")
    return ReportePaciente(
        paciente=paciente,
        citas=citas,
        progresos=progresos,
        mediciones=mediciones,
        composiciones=composiciones,
        metricas=metricas
    )

@router.get("/paciente/{id_paciente}/pdf")
def get_reporte_pdf(id_paciente: int, db: Session = Depends(get_db)):
    # Obtén datos
    reporte_data = get_reporte_paciente(id_paciente=id_paciente, db=db)
    if not reporte_data.citas:
        raise HTTPException(status_code=404, detail="No hay datos para PDF")

    # Buffer
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []

    # Estilos (azul/verde como ejemplo)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=20, spaceAfter=30, alignment=TA_CENTER, textColor=colors.darkblue)
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=14, spaceAfter=12, textColor=colors.darkgreen)

    # Header (logo placeholder, paciente, fecha, control de peso – como ejemplo)
    story.append(Paragraph("Reporte de Composición Corporal", title_style))
    story.append(Paragraph(f"Paciente: {reporte_data.paciente.nombre} {reporte_data.paciente.apellido}", heading_style))
    story.append(Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y')}", styles['Normal']))
    story.append(Paragraph(f"Control de Peso: {reporte_data.metricas['peso_final']} kg (Tendencia: {reporte_data.metricas['tendencia_peso_kg']} kg)", styles['Normal']))
    story.append(Spacer(1, 20))
    # Logo: Agrega Image('logo.png', width=1*inch, height=0.5*inch) si tienes archivo en app/

    # Tabla Medidas Básicas (fecha/peso/altura/IMC/glucosa – como ejemplo)
    story.append(Paragraph("Mediciones Básicas", heading_style))
    data_basic = [['Fecha', 'Peso (kg)', 'Altura (m)', 'IMC', 'Glucosa (mg/dL)']]
    for c in reporte_data.citas:
        data_basic.append([c.fecha.strftime('%d/%m/%Y %H:%M'), f"{c.peso:.1f}", f"{c.altura:.2f}", f"{c.imc:.1f}", f"{c.glucosa:.1f}"])
    table_basic = Table(data_basic)
    table_basic.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.darkblue)
    ]))
    story.append(table_basic)

    # Modelo de Composición Corporal (masa grasa/muscular/ósea/residual con % – como ejemplo)
    story.append(Spacer(1, 20))
    story.append(Paragraph("Modelo de Composición Corporal", heading_style))
    data_comp = [['Componente', 'Valor (kg)', '% del Total']]
    if reporte_data.composiciones:
        comp = reporte_data.composiciones[0]
        masa_grasa = comp.masa_grasa or 0
        masa_muscular = comp.masa_muscular or 0
        masa_osea = comp.masa_osea or 0
        masa_residual = comp.masa_residual or 0
        total_comp = masa_grasa + masa_muscular + masa_osea + masa_residual
        data_comp.append(['Masa Grasa', f"{masa_grasa:.1f}", f"{(masa_grasa / total_comp * 100):.1f}%"])
        data_comp.append(['Masa Muscular', f"{masa_muscular:.1f}", f"{(masa_muscular / total_comp * 100):.1f}%"])
        data_comp.append(['Masa Ósea', f"{masa_osea:.1f}", f"{(masa_osea / total_comp * 100):.1f}%"])
        data_comp.append(['Masa Residual', f"{masa_residual:.1f}", f"{(masa_residual / total_comp * 100):.1f}%"])
        data_comp.append(['Total', f"{total_comp:.1f}", '100%'])
    else:
        data_comp.append(['No hay datos', '', ''])
    table_comp = Table(data_comp)
    table_comp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.darkgreen)
    ]))
    story.append(table_comp)

    # Triángulo Somatotipo (pie chart con endomorfo/mesomorfo/ectomorfo – como ejemplo)
    story.append(Spacer(1, 20))
    story.append(Paragraph("Somatotipo", heading_style))
    pct_grasa = reporte_data.composiciones[0].porcentaje_grasa if reporte_data.composiciones else 25
    imc_prom = reporte_data.metricas['imc_promedio']
    endomorfo = pct_grasa / 10
    mesomorfo = imc_prom - endomorfo
    ectomorfo = 5 - endomorfo
    d = Drawing(400, 300)
    pc = Pie()
    pc.data = [endomorfo, mesomorfo, ectomorfo]
    pc.labels = ['Endomorfo', 'Mesomorfo', 'Ectomorfo']
    pc.x = 200
    pc.y = 150
    pc.width = 200
    pc.height = 200
    pc.slices.strokeColor = colors.black
    pc.slices.strokeWidth = 1
    pc.slices.fillColor = [HexColor('#FF6B6B'), HexColor('#4ECDC4'), HexColor('#45B7D1')]  # Rojo/azul/verde como ejemplo
    d.add(pc)
    story.append(d)

    # Histórico de Composición Corporal (barras masa muscular/grasa por cita – como ejemplo)
    story.append(Spacer(1, 20))
    story.append(Paragraph("Histórico de Composición Corporal", heading_style))
    fig, ax = plt.subplots(figsize=(8, 4))
    fechas = [c.fecha.strftime('%m/%Y') for c in reporte_data.citas]
    # Usa datos reales si múltiples composiciones; placeholder para 3 citas
    masa_musc = [reporte_data.composiciones[0].masa_muscular if i == 0 else 41.0 for i in range(len(fechas))]  # Ejemplo
    masa_grasa = [reporte_data.composiciones[0].masa_grasa if i == 0 else 21.5 for i in range(len(fechas))]
    x = range(len(fechas))
    ax.bar([i - 0.2 for i in x], masa_musc, 0.4, label='Masa Muscular', color='#4ECDC4')
    ax.bar([i + 0.2 for i in x], masa_grasa, 0.4, label='Masa Grasa', color='#FF6B6B')
    ax.set_xticks(x)
    ax.set_xticklabels(fechas)
    ax.set_ylabel('kg')
    ax.legend()
    ax.set_title('Evolución Masa Muscular vs Grasa')
    plt.xticks(rotation=45)
    img_buffer = BytesIO()
    fig.savefig(img_buffer, format='png', bbox_inches='tight')
    img_buffer.seek(0)
    story.append(Image(img_buffer, width=6*inch, height=3*inch))
    plt.close(fig)

    # Tabla Medidas Antropométricas (cintura/cadera/pliegues – como ejemplo)
    story.append(Spacer(1, 20))
    story.append(Paragraph("Medidas Antropométricas", heading_style))
    data_med = [['Medida', 'Valor (cm)']]
    if reporte_data.mediciones:
        m = reporte_data.mediciones[0]
        data_med.append(['Cintura', m.cintura])
        data_med.append(['Cadera', m.cadera])
        data_med.append(['Tríceps', m.triceps or 'N/A'])
        data_med.append(['Subescapular', m.subescapular or 'N/A'])
        data_med.append(['Suprailíaco', m.suprailiaco or 'N/A'])
        data_med.append(['Pantorrilla', m.pantorrilla or 'N/A'])
    table_med = Table(data_med)
    table_med.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightyellow),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.orange)
    ]))
    story.append(table_med)

    # Construye y devuelve
    doc.build(story)
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=reporte_paciente_{id_paciente}.pdf"})
# Opcional: Para histórico (multi-página si más datos)
@router.get("/paciente/{id_paciente}/pdf/historico")
def get_historico_pdf(id_paciente: int, db: Session = Depends(get_db)):
    # Similar, pero enfocado en histórico de evolución (gráfico línea)
    # ... código similar, con más gráficos ...
    pass