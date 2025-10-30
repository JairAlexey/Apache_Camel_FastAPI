## Evaluación Práctica – EcoLogistics S.A.

Solución de integración que demuestra la transición de File Transfer (Apache Camel) a API REST (FastAPI), cumpliendo el contrato técnico solicitado.

### Estructura

```
evaluacion-practica-ecologistics/
├── camel-lab/
│   ├── camel-file-demo/ (Proyecto Maven)
│   ├── input/envios.csv
│   ├── output/envios.json (generado por Camel)
│   └── logs en consola
├── api-rest-fastapi/
│   ├── app/
│   ├── Dockerfile
│   ├── export_openapi.py
│   ├── openapi.json
│   ├── postman_collection.json
│   ├── requirements.txt
│   └── README.md
├── README.md (general)
└── reflexion.md (convertir a PDF para entrega)
```

### Flujo esperado
1. Camel lee `envios.csv` y genera `camel-lab/output/envios.json`.
2. FastAPI arranca en puerto 8080 y carga `envios.json` en memoria.
3. Endpoints: `GET /envios`, `GET /envios/{id}`, `POST /envios`, `GET /health`.
4. Swagger UI en `/docs` y contrato en `openapi.json`.

### Ejecución

#### Camel (File Transfer y Transform)
Dentro de `camel-lab/camel-file-demo`:

```bash
mvn clean package
mvn exec:java
```

Logs esperados:
- [INFO] Archivo cargado con 3 registros.
- [INFO] Datos transformados a formato JSON.

El archivo `camel-lab/output/envios.json` será generado automáticamente.

#### FastAPI (API REST)
Desde `api-rest-fastapi`:

- Docker
```bash
docker build -t ecologistics-api .
docker run -p 8080:8080 ecologistics-api
```
- Local
```bash
pip install -r requirements.txt
python -m app.bootstrap
uvicorn app.main:app --reload --host 127.0.0.1 --port 9000```

Logs esperados en inicio:
- [INFO] API iniciada en puerto 8080.

### Stack técnico y versiones
- Java 17
- Apache Camel 4.14.1 (core, file, csv, jackson, main)
- Maven 3.9+
- Python 3.11
- FastAPI 0.115.5
- Uvicorn 0.32.0
- Pydantic 2.9.2
- Docker 24+ 

### Comandos esenciales
- Compilar/ejecutar Camel:
  - `cd camel-lab/camel-file-demo`
  - `mvn clean package`
  - `mvn exec:java`
- Ejecutar API local:
  - `cd api-rest-fastapi`
  - `pip install -r requirements.txt`
  - `uvicorn app.main:app --host 0.0.0.0 --port 8080`
- Docker API:
  - `cd api-rest-fastapi`
  - `docker build -t ecologistics-api .`
  - `docker run -p 8080:8080 ecologistics-api`

### Postman
Importar `api-rest-fastapi/postman_collection.json` y ejecutar las 3 pruebas.

### OpenAPI
Contrato en `api-rest-fastapi/openapi.json`

