from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "rodelsoft")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "RodelS0ft3566#")
MYSQL_DB = os.getenv("MYSQL_DB", "rodel_vita")

# ⚡ Deshabilitamos SSL en pymysql
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}?ssl_disabled=true"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 👉 ESTA ES LA FUNCIÓN QUE FALTABA
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
