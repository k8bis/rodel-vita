from sqlalchemy.orm import Session
import models, schemas

def get_especialistas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Especialista).offset(skip).limit(limit).all()

def get_especialista(db: Session, especialista_id: int):
    return db.query(models.Especialista).filter(models.Especialista.id_especialista == especialista_id).first()

def create_especialista(db: Session, especialista: schemas.EspecialistaCreate):
    db_especialista = models.Especialista(**especialista.dict())
    db.add(db_especialista)
    db.commit()
    db.refresh(db_especialista)
    return db_especialista

def update_especialista(db: Session, especialista_id: int, especialista: schemas.EspecialistaUpdate):
    db_especialista = get_especialista(db, especialista_id)
    if not db_especialista:
        return None
    for key, value in especialista.dict().items():
        setattr(db_especialista, key, value)
    db.commit()
    db.refresh(db_especialista)
    return db_especialista

def delete_especialista(db: Session, especialista_id: int):
    db_especialista = get_especialista(db, especialista_id)
    if not db_especialista:
        return None
    db.delete(db_especialista)
    db.commit()
    return db_especialista
