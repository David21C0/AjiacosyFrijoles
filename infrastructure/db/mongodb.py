from pymongo import MongoClient
from config import MONGO_URI, DB_NAME
from datetime import datetime

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
conversations = db["conversations"]

def find_active_conversation(phone_number):
    return conversations.find_one({
        "conversation_id": str(phone_number),  # Comparación directa (más eficiente que $regex)
        "status": "active"
    })

def update_conversation_status(conversation_id, status):
    conversations.update_one(
        {"conversation_id": str(conversation_id)},
        {
            "$set": {
                "status": status,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
def upsert_conversation(phone_number, user_msg, ai_msg):
    phone_str = str(phone_number)
    existing = find_active_conversation(phone_str)

    if existing:
        conversations.update_one(
            {"conversation_id": phone_str},
            {
                "$push": {"messages": {"$each": [user_msg, ai_msg]}},
                "$set": {
                    "updated_at": datetime.utcnow(),
                    "status": "active"
                }
            }
        )
        return "updated"
    else:
        conversations.insert_one({
            "conversation_id": phone_str,
            "messages": [user_msg, ai_msg],
            "status": "active",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        return "created"
