import pika
from datetime import datetime
from .base_client import BasicPikaClient
class FibonacciRpcServer(BasicPikaClient):
    def consume_messages(self, queue, exchange='', routing_key='', callback_func=False):
        try:
            if self.channel:
                print(" [*] " + str(datetime.now()) + " \n")
                print(' [*] Waiting for processing. To exit press CTRL+C', " \n")

                self.channel.queue_declare(queue)
                if not callback_func:
                    def callback_func(ch, method, properties, body):
                        print(" [x] Received %r" % body + " \n")
                        print("Done \n")

                self.channel.basic_qos(prefetch_count=1)
                self.channel.basic_consume(queue=routing_key, on_message_callback=callback_func, auto_ack=True)

                self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.close()
            self.connection.close()


    def get_message(self, queue):
        method_frame, header_frame, body = self.channel.basic_get(queue)
        if method_frame:
            print(method_frame, header_frame, body)
            self.channel.basic_ack(method_frame.delivery_tag)
            return method_frame, header_frame, body
        else:
            print('No message returned')
    def handle_after_consumer(self, ch, method, props, body):
        n = int(body)

        ch.basic_publish(exchange=self.exchange,
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id = \
                                                             props.correlation_id),
                         # body=str(response)
                         )
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(" [.] Process Done!")
        self.connection.close()

    # def consume_messages(self, queue):
    #     def callback(ch, method, properties, body):
    #         print(" [x] Received %r" % body)
    #
    #     self.channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
    #
    #     print(' [*] Waiting for messages. To exit press CTRL+C')
    #     self.channel.start_consuming()

