from fastapi import APIRouter, Request
from pydantic import BaseModel
from services.conversation_service import process_message

router = APIRouter()

class Mensaje(BaseModel):
    mensaje: str
    phone: str

@router.get("/")
async def root():
    return {"mensaje": "Hola desde el asistente virtual del restaurante"}

@router.post("/mensaje")
async def recibir_mensaje(request: Request):
    body = await request.json()
    print("Cuerpo crudo del request:", body)
    # Si quieres usar el modelo después:
    mensaje = Mensaje(**body)
    resultado = process_message(mensaje.phone, mensaje.mensaje)
    return resultado
