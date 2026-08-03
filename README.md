# EPIS Transparente

Sistema web para consultar y gestionar la información financiera de la Escuela Profesional de Ingeniería de Sistemas.

## Stack aprobado

- Frontend: Next.js con TypeScript.
- Backend: FastAPI con Python 3.12.
- Base de datos futura: PostgreSQL con SQLAlchemy y Alembic.
- Pruebas: Pytest (backend), Vitest (frontend) y Playwright (end-to-end, en un bloque posterior).
- Entorno local con contenedores: Docker Compose (en un bloque posterior).

La preparación actual solo expone `GET /api/health`. No incluye autenticación, PostgreSQL, migraciones ni módulos financieros.

## Estructura

- `frontend/`: aplicación Next.js y pruebas Vitest.
- `backend/`: API FastAPI, capas `routes`, `controllers`, `services`, `models`, `middleware`, `utils` y pruebas Pytest.
- `database/`, `docker/`, `docs/`: reservados para bloques posteriores.

## Requisitos

- Node.js 22 o superior y npm 10 o superior.
- Python 3.12 o superior.

## Configuración local

1. Instala las dependencias del frontend y los comandos de desarrollo:

   ```powershell
   npm.cmd install
   ```

2. Instala las dependencias del backend:

   ```powershell
   python -m pip install -e ".\backend[dev]"
   ```

3. Revisa `.env.example` y crea los archivos locales necesarios. Los valores `replace-*` son marcadores y nunca deben usarse en producción.

4. Inicia ambas aplicaciones:

   ```powershell
   npm.cmd run dev
   ```

El frontend se sirve en `http://localhost:3000` y FastAPI en `http://localhost:8000`. La salud de la API está disponible en `http://localhost:8000/api/health`.

## Variables de entorno

| Variable | Propósito |
| --- | --- |
| `ENVIRONMENT` | Entorno de ejecución de la aplicación. |
| `API_PORT` | Puerto reservado para FastAPI. |
| `FRONTEND_URL` | Origen público del frontend. |
| `NEXT_PUBLIC_API_URL` | URL pública base de la API para Next.js. |
| `DATABASE_URL` | Cadena PostgreSQL reservada para el bloque de datos. |
| `SESSION_SECRET` | Secreto reservado para autenticación. |
| `SESSION_IDLE_TIMEOUT_MINUTES` | Tiempo de sesión reservado para autenticación. |
| `STORAGE_PATH` | Ruta privada reservada para comprobantes. |

## Validaciones

| Comando | Propósito |
| --- | --- |
| `npm.cmd run build` | Compila FastAPI y construye Next.js. |
| `npm.cmd run test` | Ejecuta Pytest, Vitest y pruebas de estructura. |
| `npm.cmd run lint` | Ejecuta Ruff y ESLint. |
| `npm.cmd run format:check` | Verifica Ruff y Prettier. |
| `npm.cmd run typecheck` | Ejecuta mypy y TypeScript. |
