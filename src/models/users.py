from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.db import Base
import uuid


class Usuarios(Base):
    __tablename__ = "usuarios"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    usuario = Column(String, unique=True, nullable=False)
    numero = Column(String, unique=True, nullable=False)
    
    permisos = relationship("Permisos", back_populates="usuario")

class Webhooks(Base):
    __tablename__= "webhooks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre_weebhook = Column(String(50), nullable=False, unique=False)
    url_webhook = Column(String, nullable=False)
    estado_prueba = Column(Boolean, nullable=False)

    permisos = relationship("Permisos", back_populates="webhook")

class Permisos(Base):
    __tablename__ = "permisos"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    usuario_id = Column(String(36), ForeignKey("usuarios.id"), nullable=False)
    webhook_id = Column(String(36), ForeignKey("webhooks.id"), nullable=False)
    
    usuario = relationship("Usuarios", back_populates="permisos")
    webhook = relationship("Webhooks", back_populates="permisos")