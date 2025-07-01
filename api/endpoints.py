from fastapi import APIRouter, Request
from pydantic import BaseModel, Field
from services.conversation_service import process_message

router = APIRouter()

class From(BaseModel):
    id: int

class Message(BaseModel):
    from_: From = Field(..., alias='from')
    text: str

class TelegramUpdate(BaseModel):
    message: Message

# Endpoint que recibe el JSON desde Telegram
@router.post("/mensaje")
async def recibir_mensaje(update: TelegramUpdate):
    user_id = update.message.from_.id
    user_text = update.message.text

    resultado = process_message(user_id, user_text)

    return {"status": "ok", "resultado": resultado}