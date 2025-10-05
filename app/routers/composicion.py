from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db

router = APIRouter()  # Fix: Agrega prefix

def calculate_porcentaje_grasa(composicion: models.ComposicionCorporal, cita: models.Cita) -> float | None:
    """Helper para % grasa (evita repetición)"""
    return round((composicion.masa_grasa / float(cita.peso)) * 100, 2) if composicion.masa_grasa and cita and cita.peso else None

@router.post("/", response_model=dict)  # Mantengo dict para flexibilidad
def create_composicion(request: schemas.ComposicionCorporalCreate, db: Session = Depends(get_db)):
    # Fix: Verifica cita
    cita = db.query(models.Cita).filter(models.Cita.id_cita == request.id_cita).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    composicion = models.ComposicionCorporal(**request.dict())
    db.add(composicion)
    db.commit()
    db.refresh(composicion)
    porcentaje_grasa = calculate_porcentaje_grasa(composicion, cita)
    response = composicion.__dict__  # Fix v2: Usa __dict__ o schemas.model_dump() si ajustas schema
    response["porcentaje_grasa"] = porcentaje_grasa
    return response

@router.get("/", response_model=List[dict])  # Fix: Agrega listar todas
def get_composiciones(db: Session = Depends(get_db)):
    composiciones = db.query(models.ComposicionCorporal).all()
    # Para simplicidad, calcula solo si quieres; o expande con joins
    return [{"id_composicion": c.id_composicion, "masa_grasa": c.masa_grasa } for c in composiciones]  # Expande según necesites

@router.get("/{id}", response_model=dict)
def get_composicion(id: int, db: Session = Depends(get_db)):
    composicion = db.query(models.ComposicionCorporal).filter(models.ComposicionCorporal.id_composicion == id).first()
    if not composicion:
        raise HTTPException(status_code=404, detail="Composición no encontrada")
    cita = db.query(models.Cita).filter(models.Cita.id_cita == composicion.id_cita).first()
    porcentaje_grasa = calculate_porcentaje_grasa(composicion, cita)
    response = composicion.__dict__
    response["porcentaje_grasa"] = porcentaje_grasa
    return response

@router.get("/cita/{id_cita}", response_model=List[dict])
def get_composiciones_by_cita(id_cita: int, db: Session = Depends(get_db)):
    composicion_citas = db.query(models.ComposicionCorporal).filter(models.ComposicionCorporal.id_cita == id_cita).all()
    cita = db.query(models.Cita).filter(models.Cita.id_cita == id_cita).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return [
        {**comp.__dict__, "porcentaje_grasa": calculate_porcentaje_grasa(comp, cita)}
        for comp in composicion_citas
    ]

@router.get("/paciente/{id_paciente}", response_model=List[dict])
def get_composiciones_by_paciente(id_paciente: int, db: Session = Depends(get_db)):
    composicion_citas = (
        db.query(models.ComposicionCorporal, models.Cita)
        .join(models.Cita, models.ComposicionCorporal.id_cita == models.Cita.id_cita)
        .filter(models.Cita.id_paciente == id_paciente)
        .all()
    )
    return [
        {**comp.__dict__, "porcentaje_grasa": calculate_porcentaje_grasa(comp, cita)}
        for comp, cita in composicion_citas
    ]

# Opcional: Agrega PUT y DELETE similares a otros routers si necesitas full CRUD