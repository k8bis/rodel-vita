from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List  # Para list[]
import models, schemas  # Fix: Imports absolutos
from database import get_db  # Fix
#import models, schemas, database

router = APIRouter()

@router.post("/", response_model=schemas.Cita)
def create_cita(request: schemas.CitaCreate, db: Session = Depends(get_db)):
    pac = db.query(models.Paciente).filter(models.Paciente.id_paciente == request.id_paciente).first()
    if not pac:
        raise HTTPException(status_code=404, detail="PAciente no encontrado")
    cita = models.Cita(**request.dict())
    if cita.peso and cita.altura and cita.altura > 0:
        cita.imc = round(cita.peso / (cita.altura ** 2), 2)
    db.add(cita)
    db.commit()
    db.refresh(cita)
    return cita

@router.get("/", response_model=list[schemas.Cita])
def get_citas(db: Session = Depends(get_db)):
    return db.query(models.Cita).all()

@router.get("/{id}", response_model=schemas.Cita)
def get_cita(id: int, db: Session = Depends(get_db)):
    cita = db.query(models.Cita).filter(models.Cita.id_cita == id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return cita

@router.put("/{id}", response_model=schemas.Cita)
def update_cita(id: int, request: schemas.CitaCreate, db: Session = Depends(get_db)):
    cita = db.query(models.Cita).filter(models.Cita.id_cita == id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    for key, value in request.dict().items():
        setattr(cita, key, value)
    db.commit()
    db.refresh(cita)
    return cita

@router.delete("/{id}")
def delete_cita(id: int, db: Session = Depends(get_db)):
    cita = db.query(models.Cita).filter(models.Cita.id_cita == id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    db.delete(cita)
    db.commit()
    return {"message": "Cita eliminada"}
