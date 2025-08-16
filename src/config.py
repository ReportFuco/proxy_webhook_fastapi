from dotenv import load_dotenv
import os


load_dotenv()

# Conección a la base de datos
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Automatización ADT
WEBHOOK_ADT:str = os.getenv("WEBHOOK_ADT")

LIST_ALLOWED_ADT:list[str] = (
    os.getenv("ALLOWED_ADT")
    .split(",")
)

WEBHOOK_SAUTA:str = os.getenv("WEBHOOK_SAUTA")
NUMERO_SAUTA:str = os.getenv("NUMBER_SAUTA")

WEBHOOK_BOT = os.getenv("WEBHOOK_BOT")
WEBHOOK_SCANNER = os.getenv("WEBHOOK_SCANNER_FOTOS")

DATOS_EVOLUTION = {
    "url": os.getenv("URL_EVOLUTION_API"),
    "instance":os.getenv("INSTANCE_EVOLUTION"),
    "api_key": os.getenv("APIKEY_EVOLUTION")
}