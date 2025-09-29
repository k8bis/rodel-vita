from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database

router = APIRouter()

@router.post("/", response_model=schemas.MedicionAntropometrica)
def create_medicion(request: schemas.MedicionAntropometricaCreate, db: Session = Depends(database.get_db)):
    cita = db.query(models.Cita).filter(models.Cita.id_cita == request.id_cita).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    medicion = models.MedicionAntropometrica(**request.dict())
    db.add(medicion)
    db.commit()
    db.refresh(medicion)
    return medicion

@router.get("/{id_cita}", response_model=list[schemas.MedicionAntropometrica])
def get_mediciones(id_cita: int, db: Session = Depends(database.get_db)):
    return db.query(models.MedicionAntropometrica).filter(models.MedicionAntropometrica.id_cita == id_cita).all()

# --- Nuevo: listar por cita ---
@router.get("/cita/{id_cita}", response_model=list[schemas.MedicionAntropometrica])
def get_mediciones_by_cita(id_cita: int, db: Session = Depends(database.get_db)):
    return db.query(models.MedicionAntropometrica).filter(models.MedicionAntropometrica.id_cita == id_cita).all()

# --- Nuevo: listar por paciente ---
@router.get("/paciente/{id_paciente}", response_model=list[schemas.MedicionAntropometrica])
def get_mediciones_by_paciente(id_paciente: int, db: Session = Depends(database.get_db)):
    return (
        db.query(models.MedicionAntropometrica)
        .join(models.Cita)
        .filter(models.Cita.id_paciente == id_paciente)
        .all()
    )