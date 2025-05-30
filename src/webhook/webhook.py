from fastapi import FastAPI, Request
from loguru import logger
from producer import kafka_producer
import random
import json

logger.add("webhook.log")

app = FastAPI()


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    logger.info(f"Received data: {data}")
    kafka_producer.send(
        topic="webhook",
        key=f"{random.randrange(999)}".encode(),
        value=json.dumps({}).encode("utf-8"),
    )
    return {"message": "Webhook received successfully."}
