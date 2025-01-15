import json
import logging
import os
import random
import time
import uuid
from datetime import datetime

import pika
from pika.exchange_type import ExchangeType

# Configurações do RabbitMQ e pastas
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
PICTURAS_SRC_FOLDER = os.getenv("PICTURAS_SRC_FOLDER", "./usage_example/images/src/")
PICTURAS_OUT_FOLDER = os.getenv("PICTURAS_OUT_FOLDER", "./usage_example/images/out/")

# Configuração de logs
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
LOGGER = logging.getLogger(__name__)


def message_queue_connect():
    """
    Estabelece conexão com o RabbitMQ.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    return connection, channel


def message_queue_setup(channel):
    """
    Configura as filas e exchanges no RabbitMQ.
    """
    # Exchange principal
    channel.exchange_declare(
        exchange="picturas.tools",
        exchange_type=ExchangeType.direct,
        durable=True,
    )

    # Fila de resultados
    channel.queue_declare(queue="results")
    channel.queue_bind(
        queue="results",
        exchange="picturas.tools",
        routing_key="results",
    )

    # Fila de ChangeBrightness
    channel.queue_declare(queue="change-brightness-requests")
    channel.queue_bind(
        queue="change-brightness-requests",
        exchange="picturas.tools",
        routing_key="requests.change-brightness",
    )


def publish_request_message(channel, routing_key, request_id, procedure, parameters):
    """
    Publica uma mensagem na fila.
    """
    # Construir payload da mensagem
    message = {
        "messageId": request_id,
        "timestamp": datetime.now().isoformat(),
        "procedure": procedure,
        "parameters": parameters,
    }

    # Publicar a mensagem na exchange
    channel.basic_publish(
        exchange="picturas.tools",
        routing_key=routing_key,
        body=json.dumps(message),
    )

    logging.info("Published request '%s' to '%s'", request_id, routing_key)


def publish_mock_requests_forever():
    """
    Publica mensagens de teste para as filas configuradas.
    """
    try:
        while True:
            for file_name in os.listdir(PICTURAS_SRC_FOLDER):
                # Publicar para ChangeBrightness
                request_id_brightness = str(uuid.uuid4())
                brightness_parameters = {
                    "inputImageURI": os.path.join(PICTURAS_SRC_FOLDER, file_name),
                    "outputImageURI": os.path.join(PICTURAS_OUT_FOLDER, f"brightness_{file_name}"),
                    "brightnessFactor": random.uniform(0.5, 1.5)  # Define o fator de brilho aleatoriamente
                }
                publish_request_message(channel, "requests.change-brightness", request_id_brightness, "change_brightness", brightness_parameters)

                time.sleep(random.uniform(2, 5))  # Esperar um intervalo aleatório entre mensagens
    finally:
        connection.close()


if __name__ == "__main__":
    # Estabelecer conexão e configurar filas
    connection, channel = message_queue_connect()
    message_queue_setup(channel)

    # Publicar mensagens de teste
    publish_mock_requests_forever()
