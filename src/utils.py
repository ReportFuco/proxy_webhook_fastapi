import httpx
from src.config import *
from typing import Optional

def extract_whatsapp_info(body: dict):
    data = body.get("data", {})
    number = data.get("key", {}).get("remoteJid", "")
    conversation = data.get("message", {}).get("conversation", "")
    return number, conversation


def detectar_base64(body:dict)->Optional[tuple[str, str]]:

    base:dict = (
        body
        .get("data", {})
        .get("message", {})
    )

    caption: Optional[str] = (
    base
    .get("imageMessage", {})
    .get("caption", "")
    )   
    
    base_64: Optional[str] = (
        base  
        .get("base64", {})
    )

    return caption, base_64



def number_adt(number: str) -> bool:
    return number.replace("@s.whatsapp.net", "") in LIST_ALLOWED_ADT

async def forward_message(url: str, body: dict):
    async with httpx.AsyncClient() as client:
        await client.post(url=url, json=body)


def detectar_texto(base64_file:str):
    import base64
    import pytesseract
    from PIL import Image
    from io import BytesIO

    image_data = base64.b64decode(base64_file)
    image = Image.open(BytesIO(image_data))
    
    return pytesseract.image_to_string(image, lang="spa")


def is_number_sautita(number:str)->bool:
    return number.replace("@s.whatsapp.net", "") in NUMERO_SAUTA

async def enviar_mensaje_whatsapp(number:str, message:str):
    from bot_wsp import BotWhatsApp
    from src.config import DATOS_EVOLUTION
    bot = BotWhatsApp(**DATOS_EVOLUTION)
    
    bot.enviar_mensaje(
        numero=number, 
        mensaje="Escaneando texto...", 
        delay=300
    )
    
    bot.enviar_mensaje(
        numero=number, 
        mensaje=message, 
        delay=300
    )