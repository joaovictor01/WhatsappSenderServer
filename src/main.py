from contextlib import asynccontextmanager
import json
import random

import qrcode
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import Body, Depends, FastAPI, HTTPException, status
from loguru import logger

from auth_handler import JWTBearer, decode_jwt, sign_jwt
from controller import (
    get_user,
    insert_user,
    insert_whatsapp_message,
    get_whatsapp_messages_to_sent,
)
from models import UserLoginSchema, UserSchema, WhatsappMessage
from security import decrypt, encrypt, hash_password, verify_password
from whatsappsender import create_instance
from producer import kafka_producer

# scheduler = BackgroundScheduler()
# scheduler.add_job(get_and_update_prices, "interval", hours=1)
# scheduler.start()

# # Populando o banco de dados com os preços atuais
# get_and_update_prices()


app = FastAPI()


# Ensure the scheduler shuts down properly when application exit.
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     yield
#     scheduler.shutdown()


@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    """Cadastro nesta API. (Ao cadastrar a conta ainda estará desativada, algum admin
    do sistema precisará aprovar o cadastro.)"""
    logger.info("Creating user...")

    if get_user(user.email):
        logger.warning(f"User {user.email} already exists.")
        return {"error": "User already exists."}

    if len(user.password) < 6:
        return {"error": "Password must be at least 6 characters."}

    user.password = hash_password(user.password)
    insert_user({"allowed": False, **user.model_dump()})
    return {"message": "User created successfully."}


def check_user(data: UserLoginSchema):
    """Verifica as credenciais e se o usuário tem permissão pra utilizar esta API."""
    logger.info("Checking user credentials...")
    print(f"Data: {data}")
    user = get_user(data.email)
    if not user:
        logger.error("Dados de login incorretos.")
        return False

    if (
        user.get("email") == data.email
        and verify_password(data.password, user.get("password"))
        and user.get("allowed")
    ):
        return True

    return False


@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    """Faz login nesta API."""
    if check_user(user):
        return sign_jwt(user.email)
    return {"error": "Wrong login details!"}


@app.post("/whatsappsender/login", tags=["whatsappsender"])
async def whatsappsender_login(user: UserLoginSchema = Body(...)):
    """Cria instância do Whatsapp e faz login."""

    return {"error": "Wrong login details!"}


@app.post(
    "/whatsappsender/message",
    dependencies=[Depends(JWTBearer())],
    tags=["whatsappsender"],
)
async def send_message(message: WhatsappMessage = Body(...)):
    logger.info("Sending message...")
    # TODO: Implementar envio de mensagem via whatsapp
    kafka_producer.send(
        topic="messages",
        key=f"{random.randrange(999)}".encode(),
        value=json.dumps(
            {
                "instance": message.sender_instance,
                "recipient_number": message.receiver_number,
                "message": message.message,
            }
        ).encode("utf-8"),
    )
    return {"message": "Message sent successfully."}


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": ""}


def get_current_user(token: str = Depends(JWTBearer())):
    """
    Obtém o identificador do usuário (email) a partir do token.
    """
    payload = decode_jwt(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return user_id
