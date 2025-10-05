from pydantic import BaseModel, EmailStr, ConfigDict, Field, validator
from datetime import datetime, date
from typing import Optional


class EspecialistaBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    apellido: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    telefono: str | None = None
    especialidad: str | None = None


class EspecialistaCreate(EspecialistaBase):
    pass


class Especialista(EspecialistaBase):
    id_especialista: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PacienteBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    apellido: str = Field(..., min_length=2, max_length=100)
    fecha_nacimiento: date
    sexo: str = Field(..., pattern="^(M|F|Otro)$")
    telefono: str | None = None
    email: EmailStr | None = None


class PacienteCreate(PacienteBase):
    id_especialista: int


class Paciente(PacienteBase):
    id_paciente: int
    id_especialista: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CitaBase(BaseModel):
    fecha: datetime
    peso: float = Field(..., ge=0, le=500)
    altura: float = Field(..., ge=0.5, le=2.5)
    imc: float | None = None
    glucosa: float | None = Field(None, ge=40, le=400)
    observaciones: str | None = None


class CitaCreate(CitaBase):
    id_paciente: int
    
    @validator('imc', pre=True, always=True)
    def calculate_imc(cls, v, values):
        if 'peso' in values and 'altura' in values and values['altura'] > 0:
            return round(values['peso'] / (values['altura'] ** 2), 2 )
        return v


class Cita(CitaBase):
    id_cita: int
    id_paciente: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProgresoBase(BaseModel):
    indicador: str
    valor: float
    unidad: str | None = None


class ProgresoCreate(ProgresoBase):
    id_cita: int


class Progreso(ProgresoBase):
    id_progreso: int
    id_cita: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class MedicionAntropometricaBase(BaseModel):
    triceps: float | None = None
    subescapular: float | None = None
    suprailiaco: float | None = None
    pantorrilla: float | None = None
    diametro_biepicondilar_humero: float | None = None
    diametro_biepicondilar_femur: float | None = None
    circunferencia_brazo: float | None = None
    circunferencia_pantorrilla: float | None = None
    cintura: float = Field(..., ge=0, description="Circunferencia de cintura en cm, no puede ser negativa")
    cadera: float = Field(..., ge=0, description="Circunferencia de cadera en cm, no puede ser negativa")


class MedicionAntropometricaCreate(MedicionAntropometricaBase):
    id_cita: int

class MedicionAntropometrica(MedicionAntropometricaBase):
    id_medicion: int
    id_cita: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- Composición Corporal ---
class ComposicionCorporalBase(BaseModel):
    masa_muscular: float = Field(..., ge=0, description="Masa muscular en kg, no puede ser negativa")
    masa_grasa: float = Field(..., ge=0, description="Masa grasa en kg, no puede ser negativa")
    masa_osea: Optional[float] = None
    masa_residual: Optional[float] = None


class ComposicionCorporalCreate(ComposicionCorporalBase):
    id_cita: int


class ComposicionCorporal(ComposicionCorporalBase):
    id_composicion: int
    id_cita: int
    created_at: datetime
    porcentaje_grasa: float | None = None   # <-- solo para respuesta

    model_config = ConfigDict(from_attributes=True)
