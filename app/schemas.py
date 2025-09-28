from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date


# -------------------
# Especialista
# -------------------
class EspecialistaBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    telefono: Optional[str] = None
    especialidad: Optional[str] = None

class EspecialistaCreate(EspecialistaBase):
    pass

class EspecialistaResponse(EspecialistaBase):
    id_especialista: int
    created_at: datetime

    class Config:
        from_attributes = True


# -------------------
# Paciente
# -------------------
class PacienteBase(BaseModel):
    nombre: str
    apellido: str
    fecha_nacimiento: Optional[date] = None
    sexo: Optional[str] = "Otro"
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None

class PacienteCreate(PacienteBase):
    id_especialista: int

class PacienteResponse(PacienteBase):
    id_paciente: int
    id_especialista: int
    created_at: datetime

    class Config:
        from_attributes = True


# -------------------
# Cita
# -------------------
class CitaBase(BaseModel):
    fecha: datetime
    peso: Optional[float] = None
    altura: Optional[float] = None
    imc: Optional[float] = None
    glucosa: Optional[float] = None
    observaciones: Optional[str] = None

class CitaCreate(CitaBase):
    id_paciente: int

class CitaResponse(CitaBase):
    id_cita: int
    id_paciente: int
    created_at: datetime

    class Config:
        from_attributes = True


# -------------------
# Progreso
# -------------------
class ProgresoBase(BaseModel):
    indicador: str
    valor: float
    unidad: Optional[str] = None

class ProgresoCreate(ProgresoBase):
    id_cita: int

class ProgresoResponse(ProgresoBase):
    id_progreso: int
    id_cita: int
    created_at: datetime

    class Config:
        from_attributes = True
