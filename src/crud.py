from sqlalchemy.orm import Session, joinedload
from src.models import Usuarios, Webhooks


def obtener_nombres_usuarios(db: Session)->list[dict]:
    query = db.query(Usuarios.numero, Usuarios.permisos).all()
    return [{"usuario":r[2], "numero": r[0], "permisos": r[1]} for r in query]

def obtener_todos_urls(db: Session)->list[str]:
    query = db.query(Webhooks.url_webhook).all()
    return [r[0] for r in query]