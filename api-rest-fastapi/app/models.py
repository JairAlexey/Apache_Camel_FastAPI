from pydantic import BaseModel, Field


class Envio(BaseModel):
    id_envio: str = Field(..., description="Identificador único del envío")
    cliente: str = Field(..., description="Nombre del cliente")
    direccion: str = Field(..., description="Dirección de entrega")
    estado: str = Field(..., description="Estado actual del envío")

    class Config:
        json_schema_extra = {
            "example": {
                "id_envio": "001",
                "cliente": "Juan Pérez",
                "direccion": "Calle 12 #45",
                "estado": "En tránsito",
            }
        }
