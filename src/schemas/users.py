from pydantic import BaseModel
from typing import Optional, List


# --- Webhook ---
class WebhookBase(BaseModel):
    id: str
    nombre_weebhook: str
    url_webhook: str
    estado_prueba: bool

    class Config:
        from_attributes = True


# --- Permisos ---
class PermisoBase(BaseModel):
    id: str
    webhook: WebhookBase

    class Config:
        from_attributes = True


# --- Usuario ---
class UsuarioBase(BaseModel):
    usuario: str
    numero: str


class ListaUsuario(UsuarioBase):
    id: str
    permisos: List[PermisoBase] = []

    class Config:
        from_attributes = True


class UsuarioUpdate(BaseModel):
    usuario: Optional[str] = None
    numero: Optional[str] = None
