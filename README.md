# NominaHub

[![CI](https://github.com/vititoOX/NominaHub/actions/workflows/ci.yml/badge.svg)](https://github.com/vititoOX/NominaHub/actions/workflows/ci.yml)
![Angular](https://img.shields.io/badge/Angular-TypeScript-DD0031?logo=angular&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Python-000000?logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-SQL-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)

**ERP full stack para gestión de empleados y nóminas.**

NominaHub centraliza la información de plantilla, el cálculo de nóminas y la generación de recibos PDF en una interfaz orientada a equipos de Recursos Humanos. El proyecto está planteado como una aplicación web completa: frontend SPA, API REST, autenticación, persistencia relacional, reglas de negocio y entorno reproducible con Docker.

## Qué incluye

- Autenticación mediante JWT y perfiles de acceso.
- Dashboard con empleados activos, nóminas procesadas y coste salarial neto.
- Alta y consulta de empleados por departamento y puesto.
- Validación en frontend y backend con mensajes de error claros.
- Generación de nóminas por periodo con salario base, complementos, IRPF y Seguridad Social.
- Estados de nómina: borrador y pagada.
- Prevención de códigos, emails y nóminas duplicadas.
- Descarga de recibos en PDF mediante WeasyPrint.
- Datos iniciales de demostración para probar el flujo desde el primer arranque.
- Integración continua con build del frontend y pruebas del backend en GitHub Actions.

## Stack

| Capa | Tecnologías |
| --- | --- |
| Frontend | Angular, TypeScript, PrimeNG, PrimeIcons |
| Backend | Python, Flask, API REST, SQLAlchemy |
| Datos | PostgreSQL |
| Seguridad | JWT, hash de contraseñas, variables de entorno |
| Documentos | WeasyPrint |
| Entorno | Docker, Docker Compose |
| Calidad | Pytest, GitHub Actions |

## Arquitectura

```text
NominaHub/
├── frontend/                  # SPA Angular + PrimeNG
│   └── src/app/
├── backend/                   # API Flask REST
│   ├── app/
│   │   ├── auth.py
│   │   ├── employees.py
│   │   ├── payrolls.py
│   │   ├── dashboard.py
│   │   ├── models.py
│   │   └── pdf_service.py
│   └── tests/
├── .github/workflows/ci.yml
├── docker-compose.yml
├── .env.example
└── README.md
```

El frontend consume una API REST protegida mediante JWT. Flask concentra autenticación y lógica de negocio, SQLAlchemy gestiona la persistencia sobre PostgreSQL y WeasyPrint genera los recibos PDF en el backend.

## Inicio rápido con Docker

### Requisitos

- Docker Desktop
- Docker Compose

### 1. Configurar variables de entorno

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Linux/macOS:

```bash
cp .env.example .env
```

### 2. Levantar el proyecto

```bash
docker compose up --build
```

Servicios disponibles:

- **Frontend:** `http://localhost:4200`
- **API:** `http://localhost:5000`
- **Health check:** `http://localhost:5000/api/health`
- **PostgreSQL:** `localhost:5432`

### Usuario demo

```text
Email:      admin@nominahub.local
Contraseña: Admin123!
```

> Las credenciales de demostración y `JWT_SECRET_KEY` deben sustituirse antes de utilizar el proyecto fuera de un entorno local.

## Ejecución manual

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
flask --app run.py run --debug
```

### Frontend

En otra terminal:

```powershell
cd frontend
npm install
npm start
```

## Flujo principal

1. Iniciar sesión.
2. Consultar el resumen de plantilla y nóminas.
3. Dar de alta empleados con sus datos laborales.
4. Generar una nómina indicando empleado, periodo, IRPF y complementos.
5. Revisar bruto, deducciones y neto calculados.
6. Marcar la nómina como pagada.
7. Descargar el recibo PDF.

## Validaciones

NominaHub valida en cliente y servidor:

- Campos obligatorios de empleados y nóminas.
- Formato de email.
- Salario anual mayor que cero.
- Periodo de nómina con formato `AAAA-MM`.
- IRPF dentro del rango permitido.
- Complementos no negativos.
- Código y email de empleado duplicados.
- Nómina duplicada para el mismo empleado y periodo.

## API principal

```text
POST   /api/auth/login
GET    /api/auth/me
GET    /api/dashboard
GET    /api/employees
POST   /api/employees
GET    /api/payrolls
POST   /api/payrolls
PATCH  /api/payrolls/:id/status
GET    /api/payrolls/:id/pdf
GET    /api/health
```

## Calidad y pruebas

La integración continua comprueba automáticamente:

- Instalación limpia de dependencias del frontend con `npm ci`.
- Build de producción de Angular.
- Instalación del backend en Python 3.12.
- Prueba del health check de la API.
- Prueba del login del usuario demo.

Para ejecutar las pruebas del backend manualmente:

```powershell
cd backend
pip install -r requirements-dev.txt
pytest -q
```

## Qué demuestra este proyecto

- Diseño de una SPA profesional con Angular y componentes PrimeNG.
- Diseño y consumo de una API REST con Flask.
- Modelado relacional y persistencia con PostgreSQL y SQLAlchemy.
- Autenticación basada en JWT y tratamiento seguro de contraseñas.
- Implementación de reglas de negocio y validaciones en varias capas.
- Generación de documentos PDF desde datos persistidos.
- Contenerización del sistema completo con Docker Compose.
- Automatización básica de calidad mediante CI.

## Estado

NominaHub dispone de un flujo funcional completo de demostración: autenticación, empleados, dashboard, cálculo de nóminas, control de estado y generación de PDF. La configuración local queda aislada mediante variables de entorno y Docker Compose.
