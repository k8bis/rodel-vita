from sqlalchemy import Column, Integer, String, Date, Enum, DECIMAL, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Especialista(Base):
    __tablename__ = "especialista"

    id_especialista = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    telefono = Column(String(20))
    especialidad = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())

    pacientes = relationship("Paciente", back_populates="especialista", cascade="all, delete")


class Paciente(Base):
    __tablename__ = "paciente"

    id_paciente = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_especialista = Column(Integer, ForeignKey("especialista.id_especialista", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date)
    sexo = Column(Enum("M", "F", "Otro"), default="Otro")
    telefono = Column(String(20))
    email = Column(String(150))
    created_at = Column(DateTime, server_default=func.now())

    especialista = relationship("Especialista", back_populates="pacientes")
    citas = relationship("Cita", back_populates="paciente", cascade="all, delete")


class Cita(Base):
    __tablename__ = "cita"

    id_cita = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_paciente = Column(Integer, ForeignKey("paciente.id_paciente", ondelete="CASCADE"), nullable=False)
    fecha = Column(DateTime, nullable=False)
    peso = Column(DECIMAL(5, 2))
    altura = Column(DECIMAL(4, 2))
    imc = Column(DECIMAL(5, 2))
    glucosa = Column(DECIMAL(5, 2))
    observaciones = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    paciente = relationship("Paciente", back_populates="citas")
    progresos = relationship("Progreso", back_populates="cita", cascade="all, delete")


class Progreso(Base):
    __tablename__ = "progreso"

    id_progreso = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_cita = Column(Integer, ForeignKey("cita.id_cita", ondelete="CASCADE"), nullable=False)
    indicador = Column(String(50), nullable=False)
    valor = Column(DECIMAL(6, 2), nullable=False)
    unidad = Column(String(20))
    created_at = Column(DateTime, server_default=func.now())

    cita = relationship("Cita", back_populates="progresos")
