from fastapi import APIRouter, Request
from pydantic import BaseModel
from services.conversation_service import process_message

router = APIRouter()

class From(BaseModel):
    id: int

class Message(BaseModel):
    from_: From  # "from" es palabra reservada, por eso usamos from_
    text: str

    class Config:
        fields = {
            'from_': 'from'  # esto le dice a pydantic que "from" del JSON va a mapear a "from_"
        }

class TelegramUpdate(BaseModel):
    message: Message


@router.get("/")
async def root():
    return {"mensaje": "Hola desde el asistente virtual del restaurante"}

@router.post("/mensaje")
async def recibir_mensaje(update: TelegramUpdate):
    user_id = update.message.from_.id
    user_text = update.message.text

    # Aquí ajusta según tu lógica de negocio
    resultado = process_message(user_id, user_text)

    return {"status": "ok", "resultado": resultado}
