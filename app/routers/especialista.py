from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database

router = APIRouter(tags=["Especialistas"])

@router.post("/", response_model=schemas.Especialista)
def create_especialista(request: schemas.EspecialistaCreate, db: Session = Depends(database.get_db)):
    especialista = models.Especialista(**request.dict())
    db.add(especialista)
    db.commit()
    db.refresh(especialista)
    return especialista

@router.get("/", response_model=list[schemas.Especialista])
def get_especialistas(db: Session = Depends(database.get_db)):
    return db.query(models.Especialista).all()

@router.get("/{id}", response_model=schemas.Especialista)
def get_especialista(id: int, db: Session = Depends(database.get_db)):
    especialista = db.query(models.Especialista).filter(models.Especialista.id_especialista == id).first()
    if not especialista:
        raise HTTPException(status_code=404, detail="Especialista no encontrado")
    return especialista

@router.put("/{id}", response_model=schemas.Especialista)
def update_especialista(id: int, request: schemas.EspecialistaCreate, db: Session = Depends(database.get_db)):
    especialista = db.query(models.Especialista).filter(models.Especialista.id_especialista == id).first()
    if not especialista:
        raise HTTPException(status_code=404, detail="Especialista no encontrado")
    for key, value in request.dict().items():
        setattr(especialista, key, value)
    db.commit()
    db.refresh(especialista)
    return especialista

@router.delete("/{id}")
def delete_especialista(id: int, db: Session = Depends(database.get_db)):
    especialista = db.query(models.Especialista).filter(models.Especialista.id_especialista == id).first()
    if not especialista:
        raise HTTPException(status_code=404, detail="Especialista no encontrado")
    db.delete(especialista)
    db.commit()
    return {"message": "Especialista eliminado"}
