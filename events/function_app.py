import azure.functions as func
import logging

app = func.FunctionApp()

logger = logging.getLogger(__name__)


@app.service_bus_topic_trigger(
    arg_name="msg",
    topic_name="%SERVICE_BUS_TOPIC_NAME%",
    subscription_name="%SERVICE_BUS_SUBSCRIPTION_NAME%",
    connection="SERVICE_BUS_CONNECTION_STRING",
)
def servicebus_topic_trigger(msg: func.ServiceBusMessage):
    """Receives messages from the topic subscription and prints them to the host console."""
    body = msg.get_body()
    if isinstance(body, bytes):
        text = body.decode("utf-8")
    else:
        text = str(body)

    # Visible in `func start` terminal and in Application Insights log stream.
    print(f"[Service Bus] message body: {text}", flush=True)
    logger.info("Service Bus topic message: %s", text)
