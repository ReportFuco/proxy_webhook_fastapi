from fastapi import APIRouter, Depends, HTTPException, Request
from src.models import Webhooks
from src.db import get_db
from src.schemas import WebhookBase, WebhookCreate, WebhookConUsuarios
from sqlalchemy.orm import Session
from src.utils import extract_whatsapp_info, detectar_base64, forward_message
from src.crud import usuario_tiene_acceso_webhook, obtener_webhook_por_id
from src.middlewares.logger import logger

router = APIRouter(prefix="/webhook", tags=["webhook"])

@router.post("/")
async def proxy_webhook(request: Request, db:Session=Depends(get_db)):
    body: dict = await request.json()
    number, conversation = extract_whatsapp_info(body) 
    mensaje, base_64 = detectar_base64(body)

    number:str = number.replace("@s.whatsapp.net", "")

    # if base_64 and "extrae" in mensaje.lower() and "texto" in mensaje.lower():
    #     texto_foto = detectar_texto(base_64)
    #     await forward_message(WEBHOOK_SCANNER, body={"texto encontrado": texto_foto})
    #     await enviar_mensaje_whatsapp(number=number, message=texto_foto)
        
    if not number:
        logger.warning("No se pudo obtener el número del mensaje.")
        return {"status": "error", "detail": "remoteJid no encontrado"}

    if usuario_tiene_acceso_webhook(numero=number, db=db, webhook_id="98182190-905b-4282-8e18-db23fac0a0ae"):
        await forward_message(obtener_webhook_por_id(db=db, id="98182190-905b-4282-8e18-db23fac0a0ae"), body)

    return {"status": "usuario no permitido"}


@router.get("/{id}/usuarios", response_model=WebhookConUsuarios)
def obtener_usuarios_de_webhook(id: str, db: Session = Depends(get_db)):
    webhook = db.query(Webhooks).filter(Webhooks.id == id).first()

    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook no encontrado")

    # Extraemos usuarios a partir de los permisos
    usuarios = [permiso.usuario for permiso in webhook.permisos]

    return {
        "id": webhook.id,
        "url_webhook": webhook.url_webhook,
        "usuarios": usuarios
    }


@router.post("/agregar-webhook", response_model=WebhookBase)
def agregar_webhook(webhook: WebhookCreate, db: Session = Depends(get_db)):
    try:
        nuevo_webhook = Webhooks(**webhook.model_dump())
        db.add(nuevo_webhook)
        db.commit()
        db.refresh(nuevo_webhook)
        return nuevo_webhook
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))