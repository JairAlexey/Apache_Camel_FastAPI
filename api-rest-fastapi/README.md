## API REST EcoLogistics – Envíos (FastAPI)

### Stack técnico y versiones
- Python 3.11
- FastAPI 0.115.5
- Starlette 0.41.3
- Uvicorn 0.32.0
- Pydantic 2.9.2 / pydantic-core 2.23.4
- Docker 24+ (opcional)

### Ejecutar

Docker:
```bash
docker build -t ecologistics-api .
docker run -p 8080:8080 ecologistics-api
```

Local:
```bash
pip install -r requirements.txt
python -m app.bootstrap
uvicorn app.main:app --reload --host 127.0.0.1 --port 9000 
```

### Endpoints
- GET /health
- GET /envios
- GET /envios/{id}
- POST /envios

Swagger UI: http://localhost:9090/docs

OpenAPI export: `python export_openapi.py` -> `openapi.json`

### Comandos esenciales
- Local:
  - `pip install -r requirements.txt`
  - `uvicorn app.main:app --host 0.0.0.0 --port 8080`
- Docker:
  - `docker build -t ecologistics-api .`
  - `docker run -p 8080:8080 ecologistics-api`


