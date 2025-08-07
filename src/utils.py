import httpx
from src.config import LIST_ALLOWED_ADT

def extract_whatsapp_info(body: dict):
    data = body.get("data", {})
    number = data.get("key", {}).get("remoteJid", "")
    conversation = data.get("message", {}).get("conversation", "")
    return number, conversation

def number_adt(number: str) -> bool:
    return number.replace("@s.whatsapp.net", "") in LIST_ALLOWED_ADT

async def forward_message(url: str, body: dict):
    async with httpx.AsyncClient() as client:
        await client.post(url=url, json=body)
