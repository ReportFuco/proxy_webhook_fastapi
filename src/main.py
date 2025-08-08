from fastapi import FastAPI, Request
from src.config import *
from src.logger import logger
from src.utils import *


app = FastAPI()

@app.post("/evolution-webhook", tags=["webhook"])
async def proxy_webhook(request: Request):
    body: dict = await request.json()

    number, conversation = extract_whatsapp_info(body)
    mensaje, base_64 = detectar_base64(body)

    if base_64 and "extrae" in mensaje.lower() and "texto" in mensaje.lower():
        texto_foto = detectar_texto(base_64)
        await forward_message(WEBHOOK_SCANNER, body={"texto encontrado": texto_foto})
        await enviar_mensaje_whatsapp(number=number, message=texto_foto)
        
    if not number:
        logger.warning("No se pudo obtener el número del mensaje.")
        return {"status": "error", "detail": "remoteJid no encontrado"}

    if number_adt(number):
        await forward_message(WEBHOOK_ADT, body)
        logger.info(f"Mensaje reenviado al webhook personal desde {number}")
        return {"status": "enviado"}

    
    return {"status": "usuario no permitido"}


@app.get("/evolution-webhook", tags=["webhook"])
async def message():
    return {"status": "Método equivocado, debes usar POST"}
