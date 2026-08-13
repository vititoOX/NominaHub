# NominaHub

**Gestión de empleados y nóminas en una aplicación full stack moderna.**

NominaHub centraliza la información básica de plantilla, el cálculo de nóminas y la generación de recibos PDF en una interfaz clara orientada a equipos de Recursos Humanos.

## Funcionalidades

- Autenticación mediante JWT y perfiles de acceso.
- Dashboard con empleados activos, nóminas procesadas y coste salarial neto.
- Alta y consulta de empleados por departamento y puesto.
- Validación de formularios y mensajes de error comprensibles.
- Generación de nóminas por periodo con salario base, complementos, IRPF y Seguridad Social.
- Control de estados: borrador y pagada.
- Prevención de empleados y nóminas duplicadas.
- Descarga de recibos de nómina en PDF.
- Datos iniciales de demostración para probar el proyecto desde el primer arranque.

## Tecnologías

| Capa | Tecnologías |
| --- | --- |
| Frontend | Angular, TypeScript, PrimeNG, PrimeIcons |
| Backend | Python, Flask, API REST, SQLAlchemy |
| Datos | PostgreSQL |
| Seguridad | JWT, hash de contraseñas, variables de entorno |
| Documentos | WeasyPrint |
| Entorno | Docker, Docker Compose |

## Arquitectura

```text
NominaHub/
├── frontend/              # SPA Angular + PrimeNG
│   └── src/app/
├── backend/               # API Flask REST
│   └── app/
│       ├── auth.py
│       ├── employees.py
│       ├── payrolls.py
│       ├── dashboard.py
│       ├── models.py
│       └── pdf_service.py
├── docker-compose.yml
├── .env.example
└── README.md
```

El frontend consume la API REST protegida mediante JWT. Flask gestiona la lógica de negocio y la persistencia con SQLAlchemy sobre PostgreSQL. Los recibos se generan en el backend mediante WeasyPrint.

## Puesta en marcha con Docker

### Requisitos

- Docker Desktop
- Docker Compose

### 1. Configurar variables de entorno

En Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

En Linux/macOS:

```bash
cp .env.example .env
```

### 2. Levantar el proyecto

```bash
docker compose up --build
```

Una vez iniciado:

- **Frontend:** http://localhost:4200
- **API:** http://localhost:5000
- **Health check:** http://localhost:5000/api/health
- **PostgreSQL:** localhost:5432

### Usuario de demostración

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

1. Iniciar sesión en NominaHub.
2. Consultar el resumen de plantilla y nóminas.
3. Dar de alta empleados con sus datos laborales.
4. Generar una nómina indicando empleado, periodo, IRPF y complementos.
5. Revisar bruto, deducciones y neto calculados.
6. Marcar la nómina como pagada cuando corresponda.
7. Descargar el recibo en PDF.

## Validaciones incluidas

NominaHub valida tanto en frontend como en backend:

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
GET    /api/dashboard
GET    /api/employees
POST   /api/employees
GET    /api/payrolls
POST   /api/payrolls
PATCH  /api/payrolls/:id/status
GET    /api/payrolls/:id/pdf
GET    /api/health
```

## Estado del proyecto

El proyecto cuenta con un flujo funcional completo de demostración: autenticación, empleados, dashboard, cálculo de nóminas, cambio de estado y generación de PDF. La configuración local queda aislada mediante variables de entorno y Docker Compose.

---

Desarrollado como proyecto full stack de portfolio, poniendo el foco en arquitectura web, APIs REST, persistencia relacional y una experiencia de usuario cuidada.
