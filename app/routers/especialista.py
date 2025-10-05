from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List  # Agregado para typing
import models, schemas  # Fix: Imports absolutos
from database import get_db  # Fix

router = APIRouter()

@router.post("/", response_model=schemas.Especialista)
def create_especialista(request: schemas.EspecialistaCreate, db: Session = Depends(get_db)):
    # Opcional: Chequea email único antes de add
    if db.query(models.Especialista).filter(models.Especialista.email == request.email).first():
        raise HTTPException(status_code=400, detail="Email ya registrado")
    especialista = models.Especialista(**request.dict())
    db.add(especialista)
    db.commit()
    db.refresh(especialista)
    return especialista

@router.get("/", response_model=List[schemas.Especialista])  # Fix: List importado
def get_especialistas(db: Session = Depends(get_db)):
    return db.query(models.Especialista).all()

@router.get("/{id}", response_model=schemas.Especialista)
def get_especialista(id: int, db: Session = Depends(get_db)):
    especialista = db.query(models.Especialista).filter(models.Especialista.id_especialista == id).first()
    if not especialista:
        raise HTTPException(status_code=404, detail="Especialista no encontrado")
    return especialista

@router.put("/{id}", response_model=schemas.Especialista)
def update_especialista(id: int, request: schemas.EspecialistaCreate, db: Session = Depends(get_db)):
    especialista = db.query(models.Especialista).filter(models.Especialista.id_especialista == id).first()
    if not especialista:
        raise HTTPException(status_code=404, detail="Especialista no encontrado")
    request_dict = request.dict(exclude_unset=True)  # Fix: Solo actualiza lo enviado
    for key, value in request_dict.items():
        setattr(especialista, key, value)
    # Opcional: Re-chequea unique en update si cambias email
    if 'email' in request_dict and db.query(models.Especialista).filter(models.Especialista.email == value, models.Especialista.id_especialista != id).first():
        raise HTTPException(status_code=400, detail="Email ya registrado")
    db.commit()
    db.refresh(especialista)
    return especialista

@router.delete("/{id}")
def delete_especialista(id: int, db: Session = Depends(get_db)):
    especialista = db.query(models.Especialista).filter(models.Especialista.id_especialista == id).first()
    if not especialista:
        raise HTTPException(status_code=404, detail="Especialista no encontrado")
    db.delete(especialista)
    db.commit()
    return {"message": "Especialista eliminado"}