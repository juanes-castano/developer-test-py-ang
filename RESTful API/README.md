# Medical Image Processing API (FastAPI + PostgreSQL + Alembic)

Este proyecto implementa una API RESTful en FastAPI para gestionar resultados de procesamiento de imágenes médicas.

## 🚀 Requisitos

- Python 3.9+
- PostgreSQL
- pip

## 🛠️ Instalación

1. Clona el repositorio o descomprime el `.zip`
2. Abre una terminal en la carpeta raíz

```bash
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install -r requirements.txt
```

3. Crea el usuario de base de datos (una sola vez):

```bash
psql -U postgres -f init_user.sql
```

## 🛢️ Migraciones automáticas con Alembic

Este proyecto usa Alembic para manejar las migraciones de base de datos.

### Ya incluye la primera migración (`Initial schema`), solo debes ejecutar:

```bash
alembic upgrade head
```

Esto creará las tablas `devices` y `results` en la base de datos PostgreSQL `medical_db`.

## ▶️ Ejecutar FastAPI

```bash
uvicorn app.main:app --reload
```

## 🧠 Funcionalidad

- Validación y procesamiento automático del JSON de imágenes médicas
- Normalización, promedios, y almacenamiento en base PostgreSQL
- CRUD completo con filtros avanzados
- Logging de errores y peticiones/respuestas

## 📡 Endpoints

| Método | Ruta                  | Acción                                  |
|--------|-----------------------|-----------------------------------------|
| POST   | /api/elements/        | Crear registros desde JSON              |
| GET    | /api/elements/        | Listar todos los datos con filtros      |
| GET    | /api/elements/{id}/   | Obtener un registro por ID              |
| PUT    | /api/elements/{id}/   | Actualizar nombre de dispositivo        |
| DELETE | /api/elements/{id}/   | Eliminar un registro                    |

## 📂 Archivos importantes

- `.env`: configuración de conexión a PostgreSQL
- `init_user.sql`: script que crea el usuario `miusuario`
- `alembic/`: carpeta con control de migraciones
- `alembic.ini`: configuración del sistema de migración
- `app/`: lógica de negocio, rutas, modelos, CRUD, DB

## 🧪 Swagger UI

[http://localhost:8000/docs](http://localhost:8000/docs)
