from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional


class EspecialistaBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    telefono: Optional[str] = None
    especialidad: Optional[str] = None


class EspecialistaCreate(EspecialistaBase):
    pass


class Especialista(EspecialistaBase):
    id_especialista: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PacienteBase(BaseModel):
    nombre: str
    apellido: str
    fecha_nacimiento: Optional[datetime] = None
    sexo: Optional[str] = "Otro"
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None


class PacienteCreate(PacienteBase):
    id_especialista: int


class Paciente(PacienteBase):
    id_paciente: int
    id_especialista: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CitaBase(BaseModel):
    fecha: datetime
    peso: Optional[float] = None
    altura: Optional[float] = None
    imc: Optional[float] = None
    glucosa: Optional[float] = None
    observaciones: Optional[str] = None


class CitaCreate(CitaBase):
    id_paciente: int


class Cita(CitaBase):
    id_cita: int
    id_paciente: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProgresoBase(BaseModel):
    indicador: str
    valor: float
    unidad: Optional[str] = None


class ProgresoCreate(ProgresoBase):
    id_cita: int


class Progreso(ProgresoBase):
    id_progreso: int
    id_cita: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
