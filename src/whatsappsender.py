import os
import requests

EVOLUTION_API_BASE_URL = os.environ.get(
    "EVOLUTION_URL", "https://measured-unicorn-exact.ngrok-free.app"
)


def create_instance(phone_number: str):
    payload = {
        "instanceName": "minhainstancia",
        "token": "",
        "qrcode": True,
        "number": "5518998121995",
        "integration": "WHATSAPP-BAILEYS",
        "groups_ignore": True,
    }
    response = requests.post(EVOLUTION_API_BASE_URL + "/instance/create", json=payload)
    if response.status_code >= 200 and response.status_code < 300:
        return response.json()
