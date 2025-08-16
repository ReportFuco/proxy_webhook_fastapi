from fastapi import APIRouter, Depends, HTTPException
from src.models import Permisos
from src.schemas import PermisoCreate, PermisoBase
from sqlalchemy.orm import Session
from src.db import get_db


router = APIRouter(prefix="/permisos", tags=["Permisos"])

@router.post("/asignar-webhook", response_model=PermisoBase)
def asignar_webhook(permiso: PermisoCreate, db: Session = Depends(get_db)):
    try:
        nuevo_permiso = Permisos(**permiso.model_dump())
        db.add(nuevo_permiso)
        db.commit()
        db.refresh(nuevo_permiso)
        return nuevo_permiso
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
