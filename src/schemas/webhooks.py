from pydantic import BaseModel
from typing import List

# Para crear un webhook (lo que envías en POST)
class WebhookCreate(BaseModel):
    nombre_weebhook: str
    url_webhook: str
    estado_prueba: bool


class WebhookBase(WebhookCreate):
    id: str

    class Config:
        from_attributes = True


class UsuarioSimple(BaseModel):
    id:str
    usuario: str
    numero: str

    class Config:
        from_attributes = True


class WebhookConUsuarios(BaseModel):
    id: str
    url_webhook: str
    usuarios: List[UsuarioSimple]

    class Config:
        from_attributes = True