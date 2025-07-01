from fastapi import APIRouter, Request
from pydantic import BaseModel, Field
from services.conversation_service import process_message

router = APIRouter()


# Modelo que representa al usuario que envía el mensaje
class From(BaseModel):
    id: int

# Modelo que representa el mensaje que llega desde Telegram
class Message(BaseModel):
    from_: From = Field(..., alias="from", repr=False)
    text: str

    class Config:
        extra = "ignore"  # Ignora otros campos como chat, date, etc.
        allow_population_by_field_name = True  # Por si necesitas usar from_ en lugar de "from"

# Modelo principal que encapsula el update completo
class TelegramUpdate(BaseModel):
    message: Message

    class Config:
        extra = "ignore"

# Endpoint que recibe el webhook de Telegram
@router.post("/mensaje")
async def recibir_mensaje(update: TelegramUpdate):
    user_id = update.message.from_.id
    user_text = update.message.text

    # Aquí llamas tu lógica con los datos extraídos
    resultado = process_message(user_id, user_text)

    return {"status": "ok", "resultado": resultado}