from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database

router = APIRouter()

@router.post("/", response_model=dict)
def create_composicion(request: schemas.ComposicionCorporalCreate, db: Session = Depends(database.get_db)):
    composicion = models.ComposicionCorporal(**request.dict())
    db.add(composicion)
    db.commit()
    db.refresh(composicion)

    cita = db.query(models.Cita).filter(models.Cita.id_cita == composicion.id_cita).first()
    porcentaje_grasa = (composicion.masa_grasa / float(cita.peso)) * 100 if cita and cita.peso else None

    response = schemas.ComposicionCorporal.from_orm(composicion).model_dump()
    response["porcentaje_grasa"] = porcentaje_grasa

    return response


@router.get("/{id}", response_model=dict)
def get_composicion(id: int, db: Session = Depends(database.get_db)):
    composicion = db.query(models.ComposicionCorporal).filter(models.ComposicionCorporal.id_composicion == id).first()
    if not composicion:
        raise HTTPException(status_code=404, detail="Composición no encontrada")

    cita = db.query(models.Cita).filter(models.Cita.id_cita == composicion.id_cita).first()
    porcentaje = (composicion.masa_grasa / float(cita.peso)) * 100 if cita and cita.peso else None

    response = schemas.ComposicionCorporal.from_orm(composicion).model_dump()
    response["porcentaje_grasa"] = porcentaje

    return response


@router.get("/cita/{id_cita}", response_model=list[dict])
def get_composiciones_by_cita(id_cita: int, db: Session = Depends(database.get_db)):
    composiciones = db.query(models.ComposicionCorporal).filter(models.ComposicionCorporal.id_cita == id_cita).all()
    cita = db.query(models.Cita).filter(models.Cita.id_cita == id_cita).first()

    return [
        {
            **schemas.ComposicionCorporal.from_orm(comp).model_dump(),
            "porcentaje_grasa": (comp.masa_grasa / float(cita.peso)) * 100 if cita and cita.peso else None
        }
        for comp in composiciones
    ]


@router.get("/paciente/{id_paciente}", response_model=list[dict])
def get_composiciones_by_paciente(id_paciente: int, db: Session = Depends(database.get_db)):
    composiciones = (
        db.query(models.ComposicionCorporal, models.Cita)
        .join(models.Cita, models.ComposicionCorporal.id_cita == models.Cita.id_cita)
        .filter(models.Cita.id_paciente == id_paciente)
        .all()
    )

    return [
        {
            **schemas.ComposicionCorporal.from_orm(comp).model_dump(),
            "porcentaje_grasa": (comp.masa_grasa / float(cita.peso)) * 100 if cita and cita.peso else None
        }
        for comp, cita in composiciones
    ]
