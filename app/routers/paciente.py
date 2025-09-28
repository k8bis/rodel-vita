from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])

@router.post("/", response_model=schemas.PacienteResponse)
def create_paciente(request: schemas.PacienteCreate, db: Session = Depends(database.get_db)):
    paciente = models.Paciente(**request.dict())
    db.add(paciente)
    db.commit()
    db.refresh(paciente)
    return paciente

@router.get("/", response_model=list[schemas.PacienteResponse])
def get_pacientes(db: Session = Depends(database.get_db)):
    return db.query(models.Paciente).all()

@router.get("/{id}", response_model=schemas.PacienteResponse)
def get_paciente(id: int, db: Session = Depends(database.get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id_paciente == id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente

@router.put("/{id}", response_model=schemas.PacienteResponse)
def update_paciente(id: int, request: schemas.PacienteCreate, db: Session = Depends(database.get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id_paciente == id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    for key, value in request.dict().items():
        setattr(paciente, key, value)
    db.commit()
    db.refresh(paciente)
    return paciente

@router.delete("/{id}")
def delete_paciente(id: int, db: Session = Depends(database.get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id_paciente == id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    db.delete(paciente)
    db.commit()
    return {"message": "Paciente eliminado"}
