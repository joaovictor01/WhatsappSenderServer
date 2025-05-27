import os
from kafka import KafkaConsumer

KAFKA_PORT = os.environ.get("KAFKA_PORT", "9092")

consumer = KafkaConsumer(
    "messages",
    auto_offset_reset="earliest",
    group_id="messages-group1",
    bootstrap_servers=[f"kafka:{KAFKA_PORT}"],
)

for message in consumer:
    print(
        f"""
        topic     => {message.topic}
        partition => {message.partition}
        offset    => {message.offset}
        key={message.key} value={message.value}
    """
    )
