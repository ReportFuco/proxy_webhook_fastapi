from sqlalchemy.orm import Session
from src.models import Usuarios, Webhooks, Permisos

def obtener_nombres_usuarios(db: Session)->list[dict]:
    query = db.query(Usuarios.numero, Usuarios.permisos).all()
    return [{"usuario":r[2], "numero": r[0], "permisos": r[1]} for r in query]


def obtener_todos_urls(db: Session)->list[str]:
    query = db.query(Webhooks.url_webhook).all()
    return [r[0] for r in query]


def obtener_webhook_por_id(db:Session, id:str)->str:
    query = db.query(Webhooks.url_webhook).filter(Webhooks.id == id).first()
    return query[0]

def get_usuario_by_numero(db: Session, numero: str) -> Usuarios | None:

    return db.query(Usuarios).filter(Usuarios.numero == numero).first()


def usuario_tiene_acceso_webhook(db: Session, numero: str, webhook_id: str) -> bool:

    usuario = get_usuario_by_numero(db, numero)
    if not usuario:
        return False

    permiso = (
        db.query(Permisos)
        .filter(
            Permisos.usuario_id == usuario.id,
            Permisos.webhook_id == webhook_id
        )
        .first()
    )

    return permiso is not None