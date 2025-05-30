import os
import json
from kafka import KafkaConsumer
from loguru import logger
from whatsappsender import send_message
import threading

logger.add("consumer.log")

KAFKA_PORT = os.environ.get("KAFKA_PORT", "9092")

consumer = KafkaConsumer(
    "messages",
    auto_offset_reset="earliest",
    group_id="messages-group1",
    bootstrap_servers=[f"kafka:{KAFKA_PORT}"],
)

webhook_consumer = KafkaConsumer(
    "webhook",
    auto_offset_reset="earliest",
    group_id="webhook-group1",
    bootstrap_servers=[f"kafka:{KAFKA_PORT}"],
)

for message in consumer:
    logger.info(
        f"""
        topic     => {message.topic}
        partition => {message.partition}
        offset    => {message.offset}
        key={message.key} value={message.value}
    """
    )
    content = json.loads(message.value.decode("utf-8"))
    t = threading.Thread(
        target=send_message,
        args=(
            content.get("instance"),
            content.get("recipient_number"),
            content.get("message"),
        ),
    )
    t.start()

for message in webhook_consumer:
    logger.info(
        f"""
        topic     => {message.topic}
        partition => {message.partition}
        offset    => {message.offset}
        key={message.key} value={message.value}
    """
    )
    content = json.loads(message.value.decode("utf-8"))
    # TODO: implement handling of webhook
