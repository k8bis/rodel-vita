# 🧬redel-Vita API

**Rodel-Vita** es una API desarrollada con **FastAPI** para la gestión integral de pacientes, especialistas, citas médicas, progresos clínicos y mediciones corporales.  
Su objetivo es centralizar la información de seguimiento clínico y físico-nutricional, incluyendo composición corporal y mediciones antropométricas, para generar reportes y análisis de evolución.

---

## 🚀 Características principales

- Gestión de **especialistas** y **pacientes** vinculados.
- Registro de **citas médicas** con datos físicos (peso, altura, IMC, glucosa, observaciones).
- Seguimiento de **progresos clínicos** (indicadores y valores).
- Registro de **composición corporal** (masa muscular, grasa, ósea, residual).
- Registro de **mediciones antropométricas** (cintura, cadera, pliegues, diámetros y circunferencias).
- Cálculo automático de **porcentaje de grasa corporal** basado en la cita asociada.
- Estructura modular, preparada para expansión (reportes, autenticación, frontend).

---

## 🧱 Estructura del proyecto

```
rodel-vita/
│
├── app/
│   ├── main.py                # Punto de entrada de la aplicación FastAPI
│   ├── database.py            # Conexión a la base de datos MySQL
│   ├── models.py              # Definición de modelos SQLAlchemy
│   ├── schemas.py             # Validación y serialización Pydantic
│   └── routers/
│       ├── especialista.py    # CRUD de especialistas
│       ├── paciente.py        # CRUD de pacientes
│       ├── cita.py            # CRUD de citas
│       ├── progreso.py        # CRUD de progresos clínicos
│       ├── composicion.py     # CRUD de composición corporal
│       └── mediciones.py      # CRUD de mediciones antropométricas
│
├── Dockerfile
├── Dockerfile.prod
├── docker-compose.yml
└── README.md
```

---

## ⚙️ Configuración del entorno

### Requisitos previos
- Docker y Docker Compose instalados.
- Base de datos MySQL accesible (puede ser local o remota).
- Puerto **8001** disponible (modo desarrollo).

### Variables de entorno
Estas se definen dentro de `docker-compose.yml`:

```yaml
environment:
  - MYSQL_HOST=host.docker.internal
  - MYSQL_USER=rodelsoft
  - MYSQL_PASSWORD=RodelS0ft3566#
  - MYSQL_DB=rodel_vita
```

---

## 🐳 Ejecución con Docker

### 1️⃣ Construir e iniciar contenedores

```bash
docker-compose up --build
```

Esto iniciará los servicios:
- **api** → entorno de desarrollo (`http://localhost:8001`)
- **api-prod** → entorno de producción (`http://localhost:8002`)

### 2️⃣ Detener los contenedores

```bash
docker-compose down
```

---

## 🌐 Endpoints principales

### 🔹 Salud del servicio
```
GET /health
```
Respuesta:
```json
{"status": "ok"}
```

### 🔹 Especialistas
```
GET /especialistas/
POST /especialistas/
GET /especialistas/{id}
```

### 🔹 Pacientes
```
GET /pacientes/
POST /pacientes/
GET /pacientes/{id}
```

### 🔹 Citas
```
GET /citas/
POST /citas/
GET /citas/{id}
```

### 🔹 Progresos clínicos
```
GET /progresos/
POST /progresos/
GET /progresos/{id}
```

### 🔹 Composición corporal
```
POST /composiciones/
GET /composiciones/{id}
GET /composiciones/cita/{id_cita}
GET /composiciones/paciente/{id_paciente}
```

📘 **Nota:**  
Cada registro de composición corporal calcula automáticamente el campo `porcentaje_grasa`, pero **no se almacena** en la base de datos (se genera dinámicamente a partir de `masa_grasa` y `peso` de la cita asociada).

### 🔹 Mediciones antropométricas
```
POST /mediciones/
GET /mediciones/{id_medicion}
GET /mediciones/cita/{id_cita}
GET /mediciones/paciente/{id_paciente}
```

Campos disponibles:
- `triceps`, `subescapular`, `suprailiaco`, `pantorrilla`
- `diametro_biepicondilar_humero`, `diametro_biepicondilar_femur`
- `circunferencia_brazo`, `circunferencia_pantorrilla`
- `cintura`, `cadera`

---

## 🤪 Pruebas rápidas con HTTP files

Puedes probar los endpoints usando archivos `.http` desde VSCode o directamente con `curl`.  
Ejemplo (`test_composicion.http`):

```http
### Crear composición corporal
POST http://localhost:8001/composiciones/
Content-Type: application/json

{
  "id_cita": 1,
  "masa_grasa": 25.3,
  "masa_muscular": 38.2,
  "masa_osea": 10.1,
  "masa_residual": 12.4
}
```

---

## 🤌 Próximos pasos

- [ ] Endpoint `/reportes/paciente/{id}` consolidado.  
- [ ] Implementación de autenticación JWT.  
- [ ] Integración con frontend (panel clínico).  
- [ ] Exportación de reportes (PDF / Excel).  
- [ ] Generación automática de gráficos de evolución.  

---

## 📄 Licencia

Proyecto privado © 2025 **RodelSoft**.  
Uso interno y desarrollo en curso. No distribuido públicamente.

---
