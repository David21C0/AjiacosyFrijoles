from datetime import datetime
from domain.use_cases import should_deactivate_conversation
from infrastructure.db import mongodb
from infrastructure.ai import openai_client

def process_message(phone_number: str, user_text: str):
    existing = mongodb.find_active_conversation(phone_number)
    
    if existing:
        if should_deactivate_conversation(existing["updated_at"]):
            mongodb.update_conversation_status(existing["conversation_id"], "inactive")

    ai_reply = openai_client.get_ai_response(user_text)

    user_msg = {
        "user": "user",
        "message": user_text,
        "date_message": datetime.utcnow()
    }
    ai_msg = {
        "user": "ai",
        "message": ai_reply,
        "date_message": datetime.utcnow()
    }

    status = mongodb.upsert_conversation(phone_number, user_msg, ai_msg)

    return {
        "respuesta_ai": ai_reply,
        "status": status
    }
