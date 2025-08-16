from fastapi import APIRouter, Depends, HTTPException, Request
from src.models import Webhooks, Usuarios
from src.db import get_db
from typing import List
from src.schemas import WebhookBase, WebhookCreate, WebhookConUsuarios
from sqlalchemy.orm import Session


router = APIRouter(prefix="/webhook", tags=["webhook"])

# @router.post("/")
# async def proxy_webhook(request: Request, db:Session=Depends(get_db)):
#     body: dict = await request.json()

#     number, conversation = extract_whatsapp_info(body) 
#     mensaje, base_64 = detectar_base64(body)

#     usuario = db.query(Usuarios).filter(Usuarios.numero == number).first()


#     if base_64 and "extrae" in mensaje.lower() and "texto" in mensaje.lower():
#         texto_foto = detectar_texto(base_64)
#         await forward_message(WEBHOOK_SCANNER, body={"texto encontrado": texto_foto})
#         await enviar_mensaje_whatsapp(number=number, message=texto_foto)
        
#     if not number:
#         logger.warning("No se pudo obtener el número del mensaje.")
#         return {"status": "error", "detail": "remoteJid no encontrado"}

#     if number_adt(number):
#         await forward_message(WEBHOOK_ADT, body)
#         logger.info(f"Mensaje reenviado al webhook personal desde {number}")
#         return {"status": "enviado"}

    
#     return {"status": "usuario no permitido"}


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