from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database

router = APIRouter(prefix="/progresos", tags=["Progresos"])

@router.post("/", response_model=schemas.ProgresoResponse)
def create_progreso(request: schemas.ProgresoCreate, db: Session = Depends(database.get_db)):
    progreso = models.Progreso(**request.dict())
    db.add(progreso)
    db.commit()
    db.refresh(progreso)
    return progreso

@router.get("/", response_model=list[schemas.ProgresoResponse])
def get_progresos(db: Session = Depends(database.get_db)):
    return db.query(models.Progreso).all()

@router.get("/{id}", response_model=schemas.ProgresoResponse)
def get_progreso(id: int, db: Session = Depends(database.get_db)):
    progreso = db.query(models.Progreso).filter(models.Progreso.id_progreso == id).first()
    if not progreso:
        raise HTTPException(status_code=404, detail="Progreso no encontrado")
    return progreso

@router.put("/{id}", response_model=schemas.ProgresoResponse)
def update_progreso(id: int, request: schemas.ProgresoCreate, db: Session = Depends(database.get_db)):
    progreso = db.query(models.Progreso).filter(models.Progreso.id_progreso == id).first()
    if not progreso:
        raise HTTPException(status_code=404, detail="Progreso no encontrado")
    for key, value in request.dict().items():
        setattr(progreso, key, value)
    db.commit()
    db.refresh(progreso)
    return progreso

@router.delete("/{id}")
def delete_progreso(id: int, db: Session = Depends(database.get_db)):
    progreso = db.query(models.Progreso).filter(models.Progreso.id_progreso == id).first()
    if not progreso:
        raise HTTPException(status_code=404, detail="Progreso no encontrado")
    db.delete(progreso)
    db.commit()
    return {"message": "Progreso eliminado"}
