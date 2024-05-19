import pika
import uuid

class StarSignClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        # Declare a unique response queue for this client instance
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

        self.response = None
        self.correlation_id = None

    def on_response(self, ch, method, properties, body):
        if self.correlation_id == properties.correlation_id:
            self.response = body.decode()

    def send_star_sign(self, star_sign):
        self.response = None
        self.correlation_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=star_sign,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.correlation_id,
            )
        )
        while self.response is None:
            self.connection.process_data_events()
        return self.response

if __name__ == '__main__':
    star_sign_client = StarSignClient()
    star_sign = input("Enter your star sign: ").strip()
    response = star_sign_client.send_star_sign(star_sign)
    print(f"Response: {response}")
