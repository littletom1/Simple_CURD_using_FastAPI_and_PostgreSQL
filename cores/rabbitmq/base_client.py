import ssl
import pika
from decouple import config
import traceback
import logging
LOG = logging.getLogger(__name__)
class BasicPikaClient:
    host = config('RABBITMQ_HOST')
    port = config('RABBITMQ_PORT')
    user = config('RABBITMQ_USER')
    password = config('RABBITMQ_PASS')
    vhost = config('RABBITMQ_VHOST')
    def __init__(self):

        # # SSL Context for TLS configuration of Amazon MQ for RabbitMQ
        # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        # ssl_context.set_ciphers('ECDHE+AESGCM:!ECDSA')
        #
        # url = f"amqps://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_broker_id}.mq.{region}.amazonaws.com:5671"
        # parameters = pika.URLParameters(url)
        # parameters.ssl_options = pika.SSLOptions(context=ssl_context)
        self._initiateConnection()


    def _initiateConnection(self):
        LOG.debug('Connecting to rabbitmq server')
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host))

            self.channel = self.connection.channel()
        except Exception as e:
            self.channel = None
            LOG.error(e)
            LOG.debug(traceback.format_exc())
            print('Connection fail. Please check rabbitmq-server is running.')

    def close(self):
        self.channel.close()
        self.connection.close()