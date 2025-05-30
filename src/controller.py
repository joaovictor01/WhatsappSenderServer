import os

# from datetime import datetime

import pymongo
from loguru import logger

logger.add("logs_whatsappsenderserver.log")

mongo_connection_str = os.environ.get(
    "mongo_connection",
    (
        f"mongodb://{os.environ.get('MONGO_USERNAME')}:"
        f"{os.environ.get('MONGO_PASSWORD')}@mongo:27017"
    ),
)


def get_db():
    client = pymongo.MongoClient(mongo_connection_str)
    db = client["db_api_wppsenderserver"]
    return db


def insert_user(user_data: dict):
    db = get_db()
    users = db["users"]
    users.insert_one(user_data)


def get_user(email: str):
    db = get_db()
    users = db["users"]
    return users.find_one({"email": email})


def insert_whatsapp_message(whatsapp_message: dict):
    db = get_db()
    whatsapp_messages = db["whatsapp_messages"]
    whatsapp_messages.insert_one(whatsapp_message)


def get_whatsapp_messages_to_sent():
    db = get_db()
    whatsapp_messages = db["whatsapp_messages"]
    return whatsapp_messages.find({"sent": False})
