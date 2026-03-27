import json
import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Protocol

from azure.servicebus import ServiceBusClient, ServiceBusMessage

logger = logging.getLogger(__name__)


class MessagePublisher(Protocol):
    def publish(self, body: str) -> None: ...


class ServiceBusTopicPublisher:
    def __init__(self, connection_string: str, topic_name: str) -> None:
        self._connection_string = connection_string
        self._topic_name = topic_name

    def publish(self, body: str) -> None:
        with ServiceBusClient.from_connection_string(self._connection_string) as client:
            with client.get_topic_sender(topic_name=self._topic_name) as sender:
                sender.send_messages(ServiceBusMessage(body))


def say_hello_and_publish(
    message: str = "hello world",
    metadata: Optional[Dict[str, Any]] = None,
    publisher: Optional[MessagePublisher] = None,
) -> Dict[str, Any]:
    payload = {
        "message": message,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    if metadata:
        payload["metadata"] = metadata

    message_body = json.dumps(payload)

    try:
        if publisher is None:
            connection_string = os.getenv("SERVICE_BUS_CONNECTION_STRING", "")
            print(f"CONNECTION STRING: {connection_string}")
            topic_name = os.getenv("SERVICE_BUS_TOPIC_NAME", "")
            print(f"TOPIC NAME: {topic_name}")
            if not connection_string or not topic_name:
                raise ValueError(
                    "Missing SERVICE_BUS_CONNECTION_STRING or SERVICE_BUS_TOPIC_NAME"
                )
            publisher = ServiceBusTopicPublisher(connection_string, topic_name)

        publisher.publish(message_body)
        return {
            "ok": True,
            "message": "hello published",
            "payload": payload,
            "error": None,
        }
    except Exception as exc:
        logger.exception("Failed to publish hello message to Service Bus topic")
        return {
            "ok": False,
            "message": "publish failed",
            "payload": payload,
            "error": str(exc),
        }
