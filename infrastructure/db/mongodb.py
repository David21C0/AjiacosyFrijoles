from pymongo import MongoClient
from config import MONGO_URI, DB_NAME
from datetime import datetime

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
conversations = db["conversations"]

def find_active_conversation(phone_number):
    return conversations.find_one({"conversation_id": {"$regex": phone_number}, "status": "active"})

def update_conversation_status(conversation_id, status):
    conversations.update_one({"conversation_id": conversation_id}, {"$set": {"status": status, "updated_at": datetime.utcnow()}})

def upsert_conversation(phone_number, user_msg, ai_msg):
    existing = find_active_conversation(phone_number)
    if existing:
        conversations.update_one(
            {"conversation_id": {"$regex": phone_number}},
            {
                "$push": {"messages": {"$each": [user_msg, ai_msg]}},
                "$set": {"updated_at": datetime.utcnow(), "status": "active"}
            }
        )
        return "updated"
    else:
        conversations.insert_one({
            "conversation_id": phone_number,
            "messages": [user_msg, ai_msg],
            "status": "active",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        return "created"
