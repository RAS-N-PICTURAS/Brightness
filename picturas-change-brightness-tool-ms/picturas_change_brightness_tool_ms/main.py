import logging

from .config import PICTURAS_LOG_LEVEL
from .core.message_processor import MessageProcessor
from .core.message_queue_setup import message_queue_connect
from .change_brightness_request_message import ChangeBrightnessRequestMessage
from .change_brightness_result_message import ChangeBrightnessResultMessage
from .change_brightness_tool import ChangeBrightnessTool

# Logging setup
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
logging.basicConfig(level=PICTURAS_LOG_LEVEL, format=LOG_FORMAT)

LOGGER = logging.getLogger(__name__)

if __name__ == "__main__":
    # Conectar ao RabbitMQ
    connection, channel = message_queue_connect()

    # Configurar a ferramenta, mensagens e processador
    tool = ChangeBrightnessTool()
    request_msg_class = ChangeBrightnessRequestMessage
    result_msg_class = ChangeBrightnessResultMessage

    message_processor = MessageProcessor(tool, request_msg_class, result_msg_class, channel)

    try:
        LOGGER.info("Starting the ChangeBrightness tool...")
        message_processor.start()
    except KeyboardInterrupt:
        LOGGER.info("Stopping the ChangeBrightness tool...")
        message_processor.stop()
    finally:
        connection.close()
        LOGGER.info("Connection closed.")
