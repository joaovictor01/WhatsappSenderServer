import os
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

for message in consumer:
    logger.info(
        f"""
        topic     => {message.topic}
        partition => {message.partition}
        offset    => {message.offset}
        key={message.key} value={message.value}
    """
    )
    content = message.value
    t = threading.Thread(
        target=send_message,
        args=(
            content.get("instance"),
            content.get("recipient_number"),
            content.get("message"),
        ),
    )
    t.start()
