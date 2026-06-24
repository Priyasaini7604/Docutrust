from pymongo import MongoClient
from core.config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
chat_collection = db["chats"]
document_collection = db["documents"]