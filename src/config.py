from dotenv import load_dotenv
import os


load_dotenv()

# Automatización ADT
WEBHOOK_ADT:str = os.getenv("WEBHOOK_ADT")

LIST_ALLOWED_ADT:list[str] = (
    os.getenv("ALLOWED_ADT")
    .split(",")
)
