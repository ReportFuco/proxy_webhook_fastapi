from fastapi import FastAPI, Request
from src.config import WEBHOOK_ADT
from src.logger import logger
from src.utils import *


app = FastAPI()

@app.post("/evolution-webhook", tags=["webhook"])
async def proxy_webhook(request: Request):
    body: dict = await request.json()

    number, conversation = extract_whatsapp_info(body)

    logger.info(f"Mensaje recibido de: {number} - Contenido: '{conversation}'")

    if not number:
        logger.warning("No se pudo obtener el número del mensaje.")
        return {"status": "error", "detail": "remoteJid no encontrado"}

    if number_adt(number):
        await forward_message(WEBHOOK_ADT, body)
        logger.info(f"Mensaje reenviado al webhook personal desde {number}")
        return {"status": "enviado"}

    logger.warning(f"Número no autorizado: {number}")
    return {"status": "usuario no permitido"}


@app.get("/evolution-webhook", tags=["webhook"])
async def message():
    return {"status": "Método equivocado, debes usar POST"}
