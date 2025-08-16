from fastapi import FastAPI
from src.routes.users import router as users_router
from src.routes.webhook import router as webhook_router
from src.routes.permisos import router as permisos_router

app = FastAPI()

# Rutas
app.include_router(users_router)
app.include_router(webhook_router)
app.include_router(permisos_router)

@app.get("/")
def root():
    return {"info": "Bienvenido al proxy para Evolution API y n8n"}
