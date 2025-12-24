import os
import requests
from loguru import logger

logger.add("whatsappsender.log")

EVOLUTION_API_BASE_URL = os.environ.get("EVOLUTION_URL", "evolution-api")


def create_instance(phone_number: str):
    payload = {
        "instanceName": phone_number,
        "token": "",
        "qrcode": True,
        "number": phone_number,
        "integration": "WHATSAPP-BAILEYS",
        "groups_ignore": True,
    }
    response = requests.post(EVOLUTION_API_BASE_URL + "/instance/create", json=payload)
    if response.status_code >= 200 and response.status_code < 300:
        return response.json()


def send_message(instance: str, phone_number: str, message: str):
    payload = {"number": phone_number, "text": message}
    headers = {"apikey": os.environ.get("AUTHENTICATION_API_KEY")}
    response = requests.post(
        f"{EVOLUTION_API_BASE_URL}/message/sendText/{instance}",
        json=payload,
        headers=headers,
    )
    if response.status_code >= 200 and response.status_code < 300:
        logger.info("Message sent successfully.")
        return response.json()

    logger.error("Failed to send message.")
    logger.error(response.content)
    return None
