from src.schemas import UsuarioBase, UsuarioUpdate, ListaUsuario
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models import Usuarios
from src.db import get_db
from typing import List


# Iniciar router
router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# Extraer todos los usuarios
@router.get("/", response_model=List[ListaUsuario])
def obtener_usuarios(db:Session = Depends(get_db)):
    return db.query(Usuarios).all()


# Extraer un usuario especifico con ID
@router.get("/{id}", response_model=ListaUsuario)
def obtener_usuario_id(id: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuarios).filter(Usuarios.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


# Crear nuevo usuario
@router.post("/crear-usuario", response_model=UsuarioBase)
def crear_usuarios(usuario:UsuarioBase, db:Session = Depends(get_db)):
    try:
        nuevo_usuario = Usuarios(**usuario.model_dump())
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)

        return nuevo_usuario 
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# Modificar un usuario entregando el ID
@router.put("/{id}", response_model=UsuarioBase)
def modificar_usuario(id: str, cambio: UsuarioUpdate, db: Session = Depends(get_db)):
    try:
        update_user = db.query(Usuarios).filter(Usuarios.id == id).first()
        if not update_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        data = cambio.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(update_user, key, value)

        db.commit()
        db.refresh(update_user)
        return update_user

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# Eliminar el usuario a través del ID
@router.delete("/{id}")
def eliminar_usuario(id: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuarios).filter(Usuarios.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario)
    db.commit()
    return {"message": "Usuario eliminado correctamente"}