from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas  # Fix: Absolutos
from database import get_db  # Fix

router = APIRouter()  # Fix: Prefix y tags

@router.post("/", response_model=schemas.MedicionAntropometrica)
def create_medicion(request: schemas.MedicionAntropometricaCreate, db: Session = Depends(get_db)):
    cita = db.query(models.Cita).filter(models.Cita.id_cita == request.id_cita).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    medicion = models.MedicionAntropometrica(**request.dict())
    db.add(medicion)
    db.commit()
    db.refresh(medicion)
    return medicion

@router.get("/", response_model=List[schemas.MedicionAntropometrica])  # Fix: Agrega listar todas
def get_mediciones(db: Session = Depends(get_db)):
    return db.query(models.MedicionAntropometrica).all()

@router.get("/{id_medicion}", response_model=schemas.MedicionAntropometrica)  # Fix: Por ID de medicion, no cita
def get_medicion(id_medicion: int, db: Session = Depends(get_db)):
    medicion = db.query(models.MedicionAntropometrica).filter(models.MedicionAntropometrica.id_medicion == id_medicion).first()
    if not medicion:
        raise HTTPException(status_code=404, detail="Medición no encontrada")
    return medicion

@router.get("/cita/{id_cita}", response_model=List[schemas.MedicionAntropometrica])
def get_mediciones_by_cita(id_cita: int, db: Session = Depends(get_db)):
    return db.query(models.MedicionAntropometrica).filter(models.MedicionAntropometrica.id_cita == id_cita).all()

@router.get("/paciente/{id_paciente}", response_model=List[schemas.MedicionAntropometrica])
def get_mediciones_by_paciente(id_paciente: int, db: Session = Depends(get_db)):
    return (
        db.query(models.MedicionAntropometrica)
        .join(models.Cita)
        .filter(models.Cita.id_paciente == id_paciente)
        .all()
    )

# Opcional: PUT y DELETE (similar a otros routers)
@router.put("/{id_medicion}", response_model=schemas.MedicionAntropometrica)
def update_medicion(id_medicion: int, request: schemas.MedicionAntropometricaCreate, db: Session = Depends(get_db)):
    medicion = db.query(models.MedicionAntropometrica).filter(models.MedicionAntropometrica.id_medicion == id_medicion).first()
    if not medicion:
        raise HTTPException(status_code=404, detail="Medición no encontrada")
    request_dict = request.dict(exclude_unset=True, exclude={'id_cita'})  # Fix: No sobrescribir id_cita
    for key, value in request_dict.items():
        setattr(medicion, key, value)
    db.commit()
    db.refresh(medicion)
    return medicion

@router.delete("/{id_medicion}")
def delete_medicion(id_medicion: int, db: Session = Depends(get_db)):
    medicion = db.query(models.MedicionAntropometrica).filter(models.MedicionAntropometrica.id_medicion == id_medicion).first()
    if not medicion:
        raise HTTPException(status_code=404, detail="Medición no encontrada")
    db.delete(medicion)
    db.commit()
    return {"message": "Medición eliminada"}