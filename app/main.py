# app/main.py
from fastapi import FastAPI
from routers import especialista, paciente, cita, progreso

app = FastAPI(title="Rodel-Vita API")

# Rutas principales
@app.get("/")
def root():
    return {"message": "Bienvenido a Rodel-Vita API 🚀"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Incluir routers con prefijos y tags claros
app.include_router(especialista.router, prefix="/especialistas", tags=["Especialistas"])
app.include_router(paciente.router, prefix="/pacientes", tags=["Pacientes"])
app.include_router(cita.router, prefix="/citas", tags=["Citas"])
app.include_router(progreso.router, prefix="/progresos", tags=["Progresos"])
