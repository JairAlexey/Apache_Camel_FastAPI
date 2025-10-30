from __future__ import annotations

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .models import Envio
from .storage import storage


def create_app() -> FastAPI:
    app = FastAPI(
        title="API REST EcoLogistics – Envíos (FastAPI)",
        version="1.0.0",
        description=(
            "API para gestión de envíos de EcoLogistics S.A. "
            "Carga envios.json, permite consultas y creación, y persiste cambios."
        ),
        contact={
            "name": "Autor",
        },
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def on_startup() -> None:
        print("[INFO] API iniciada en puerto 8080.")

    @app.get("/health", summary="Health check")
    def health() -> dict:
        return {"status": "ok"}

    @app.get("/envios", response_model=list[Envio], summary="Lista todos los envíos")
    def listar_envios() -> list[Envio]:
        return storage.list_envios()

    @app.get(
        "/envios/{envio_id}",
        response_model=Envio,
        responses={404: {"description": "Envío no encontrado"}},
        summary="Obtiene un envío por ID",
    )
    def obtener_envio(envio_id: str) -> Envio:
        envio = storage.get_envio(envio_id)
        if envio is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Envío no encontrado")
        return envio

    @app.post(
        "/envios",
        response_model=Envio,
        status_code=status.HTTP_201_CREATED,
        responses={409: {"description": "ID ya existe"}},
        summary="Crea un nuevo envío",
    )
    def crear_envio(envio: Envio) -> JSONResponse:
        creado = storage.create_envio(envio)
        if not creado:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El ID ya existe")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=envio.model_dump())

    return app


app = create_app()
