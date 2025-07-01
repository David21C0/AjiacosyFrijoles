from fastapi import FastAPI
from api.endpoints import router as api_router
import asyncio
from infrastructure.db import mongodb
from domain.use_cases import should_deactivate_conversation
from datetime import datetime

app = FastAPI()
app.include_router(api_router)

async def verificar_conversaciones_inactivas():
    while True:
        conversaciones = mongodb.conversations.find({"status": "active"})
        for conv in conversaciones:
            if should_deactivate_conversation(conv["updated_at"]):
                mongodb.update_conversation_status(conv["conversation_id"], "inactive")
                print(f"Conversación {conv['conversation_id']} marcada como inactiva")
        await asyncio.sleep(30)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(verificar_conversaciones_inactivas())
