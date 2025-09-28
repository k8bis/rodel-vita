from fastapi import FastAPI
import models, database
from routers import especialista, paciente, cita, progreso

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Rodel-Vita API 🚀")

@app.get("/")
def root():
    return {"message": "Bienvenido a Rodel-Vita API 🚀"}

app.include_router(especialista.router)
app.include_router(paciente.router)
app.include_router(cita.router)
app.include_router(progreso.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
