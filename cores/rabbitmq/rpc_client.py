import pika
import uuid
from .base_client import BasicPikaClient
class FibonacciRpcClient(BasicPikaClient):
    def __init__(self):
        super().__init__()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
    def send_message(self, body, header={},  method='', routing_key='', print_message=True):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=routing_key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
                type=method,
                headers= header
            ),
            body=str(body))
        # self.connection.process_data_events(time_limit=None)
        if print_message:
            print(f"Sent message. Method: {method}, Routing Key: {routing_key}, Body: {body}")
        self.connection.close()
        return (f"Sent message. Method: {method}, Routing Key: {routing_key}, Body: {body}")
