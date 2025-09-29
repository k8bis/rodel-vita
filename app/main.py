from fastapi import FastAPI, Depends
from routers import especialista, paciente, cita, progreso, composicion, mediciones
#from auth import get_current_user

app = FastAPI(title="Rodel-Vita API")

@app.get("/")
def root():
    return {"message": "Bienvenido a Rodel-Vita API 🚀"}

@app.get("/health")
def health_check():
    return {"status": "ok"}


# Incluir routers protegidos
#app.include_router(
#   especialista.router, prefix="/especialistas", tags=["Especialistas"],
#    dependencies=[Depends(get_current_user)]
#)
#app.include_router(
#    paciente.router, prefix="/pacientes", tags=["Pacientes"],
#    dependencies=[Depends(get_current_user)]
#)
#app.include_router(
#    cita.router, prefix="/citas", tags=["Citas"],
#    dependencies=[Depends(get_current_user)]
#)
#app.include_router(
#    progreso.router, prefix="/progresos", tags=["Progresos"],
#    dependencies=[Depends(get_current_user)]
#)
# Incluir routers sin protección
app.include_router(
    especialista.router, prefix="/especialistas", tags=["Especialistas"]
)
app.include_router(
    paciente.router, prefix="/pacientes", tags=["Pacientes"]
)
app.include_router(
    cita.router, prefix="/citas", tags=["Citas"]
)
app.include_router(
    progreso.router, prefix="/progresos", tags=["Progresos"]
)

app.include_router(
    composicion.router, prefix="/composiciones", tags=["Composición Corporal"]
)

app.include_router(
    mediciones.router, prefix="/mediciones", tags=["Mediciones Antropométricas"]
)
