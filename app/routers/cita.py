from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database

router = APIRouter(prefix="/citas", tags=["Citas"])

@router.post("/", response_model=schemas.Cita)
def create_cita(request: schemas.CitaCreate, db: Session = Depends(database.get_db)):
    cita = models.Cita(**request.dict())
    db.add(cita)
    db.commit()
    db.refresh(cita)
    return cita

@router.get("/", response_model=list[schemas.Cita])
def get_citas(db: Session = Depends(database.get_db)):
    return db.query(models.Cita).all()

@router.get("/{id}", response_model=schemas.Cita)
def get_cita(id: int, db: Session = Depends(database.get_db)):
    cita = db.query(models.Cita).filter(models.Cita.id_cita == id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return cita

@router.put("/{id}", response_model=schemas.Cita)
def update_cita(id: int, request: schemas.CitaCreate, db: Session = Depends(database.get_db)):
    cita = db.query(models.Cita).filter(models.Cita.id_cita == id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    for key, value in request.dict().items():
        setattr(cita, key, value)
    db.commit()
    db.refresh(cita)
    return cita

@router.delete("/{id}")
def delete_cita(id: int, db: Session = Depends(database.get_db)):
    cita = db.query(models.Cita).filter(models.Cita.id_cita == id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    db.delete(cita)
    db.commit()
    return {"message": "Cita eliminada"}
