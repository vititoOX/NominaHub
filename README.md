# NominaHub

ERP full stack de gestión de empleados y nóminas orientado a portfolio profesional.

## Stack

- Angular + TypeScript + PrimeNG
- Python + Flask + API REST
- PostgreSQL + SQLAlchemy
- JWT y control de roles
- WeasyPrint para recibos PDF
- Docker Compose

## Funcionalidades

- Login JWT con roles `admin` y `rrhh`
- Dashboard con KPIs de plantilla y coste salarial
- Alta y consulta de empleados
- Generación de nóminas con salario base, complementos, IRPF y Seguridad Social
- Estado borrador/pagada
- Descarga de recibos PDF
- Datos demo automáticos en desarrollo

## Arranque con Docker

```bash
cp .env.example .env
docker compose up --build
```

- Frontend: http://localhost:4200
- API: http://localhost:5000/api/health

Usuario demo: `admin@nominahub.local` / `Admin123!`

> Cambia las credenciales y `JWT_SECRET_KEY` antes de cualquier despliegue real.

## Arranque manual

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
flask --app run.py run --debug
```

### Frontend

```bash
cd frontend
npm install
npm start
```
