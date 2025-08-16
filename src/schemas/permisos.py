from pydantic import BaseModel


class PermisoCreate(BaseModel):
    usuario_id: str
    webhook_id: str


class PermisoBase(PermisoCreate):
    id: str
    class Config:
        from_attributes = True
