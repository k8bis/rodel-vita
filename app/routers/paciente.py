from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db
#import models, schemas, database

router = APIRouter()

@router.post("/", response_model=schemas.Paciente)
def create_paciente(request: schemas.PacienteCreate, db: Session = Depends(get_db)):
    espec = db.query(models.Especialista).filter(models.Especialista.id_especialista == request.id_especialista).first()
    if not espec:
        raise HTTPException(status_code=404, detail= "Especialista no encontrado")
    paciente = models.Paciente(**request.dict())
    db.add(paciente)
    db.commit()
    db.refresh(paciente)
    return paciente

@router.get("/", response_model=list[schemas.Paciente])
def get_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

@router.get("/{id}", response_model=schemas.Paciente)
def get_paciente(id: int, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id_paciente == id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente

@router.put("/{id}", response_model=schemas.Paciente)
def update_paciente(id: int, request: schemas.PacienteCreate, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id_paciente == id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    request_dict = request.dict(exclude_unset=True)
    for key, value in request.dict().items():
        setattr(paciente, key, value)
    db.commit()
    db.refresh(paciente)
    return paciente

@router.delete("/{id}")
def delete_paciente(id: int, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id_paciente == id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    db.delete(paciente)
    db.commit()
    return {"message": "Paciente eliminado"}
