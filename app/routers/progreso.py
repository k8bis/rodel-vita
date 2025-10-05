from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Progreso)
def create_progreso(request: schemas.ProgresoCreate, db: Session = Depends(get_db)):
    # Fix: Verifica cita existe
    cita = db.query(models.Cita).filter(models.Cita.id_cita == request.id_cita).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    progreso = models.Progreso(**request.dict())
    db.add(progreso)
    db.commit()
    db.refresh(progreso)
    return progreso

@router.get("/", response_model=List[schemas.Progreso])
def get_progresos(db: Session = Depends(get_db)):
    return db.query(models.Progreso).all()

@router.get("/{id}", response_model=schemas.Progreso)
def get_progreso(id: int, db: Session = Depends(get_db)):
    progreso = db.query(models.Progreso).filter(models.Progreso.id_progreso == id).first()
    if not progreso:
        raise HTTPException(status_code=404, detail="Progreso no encontrado")
    return progreso

@router.put("/{id}", response_model=schemas.Progreso)
def update_progreso(id: int, request: schemas.ProgresoCreate, db: Session = Depends(get_db)):
    progreso = db.query(models.Progreso).filter(models.Progreso.id_progreso == id).first()
    if not progreso:
        raise HTTPException(status_code=404, detail="Progreso no encontrado")
    request_dict = request.dict(exclude_unset=True)  # Fix
    for key, value in request_dict.items():
        setattr(progreso, key, value)
    db.commit()
    db.refresh(progreso)
    return progreso

@router.delete("/{id}")
def delete_progreso(id: int, db: Session = Depends(get_db)):
    progreso = db.query(models.Progreso).filter(models.Progreso.id_progreso == id).first()
    if not progreso:
        raise HTTPException(status_code=404, detail="Progreso no encontrado")
    db.delete(progreso)
    db.commit()
    return {"message": "Progreso eliminado"}