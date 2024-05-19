import pika

# Define the RabbitMQ server address
rabbitmq_host = 'localhost'

# Define the queue name
queue_name = 'task_queue'

# Define star sign messages
star_sign_messages = {
    'aries': 'Stick with what you know works for your skin, it can be confusing to try every new skincare trend.',
    'taurus': 'Brava taurus! You look fabulous, your routine will have you looking 30 when you are 50.',
    'gemini': 'It might be hard for you, but try to let your natural beauty shine through.',
    'cancer': 'You might need more than one cleanser open at a time. Let your skin tell you what it needs.',
    'leo': 'WEAR. SUNSCREEN.',
    'virgo': 'It is ok to treat yourself sometimes! Try a nourishing face mask.',
    'libra': 'Separate eye creams are ok but most serums can be taken around the eye area safely.',
    'scorpio': 'Always take your make-up off: micellar water, double cleansing whatever, just DO IT.',
    'sagittarius': 'A facial every now and then is not a replacement for a sensible daily regime at home.',
    'capricorn': 'Please notice if your skin needs hydration, try a mist, essence or facial oil.',
    'aquarius': 'If you dabble in acids or retinol, remember to hydrate carefully!',
    'pisces': 'Try a light serum and a moisturising SPF instead of separate hydration steps.',
}

def callback(ch, method, properties, body):
    star_sign = body.decode()
    response = star_sign_messages.get(star_sign.lower(), "Unknown star sign")

    # Send the response back to the client
    response_channel = ch.connection.channel()
    response_channel.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        body=response,
        properties=pika.BasicProperties(
            correlation_id=properties.correlation_id,
        )
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    channel.start_consuming()

if __name__ == '__main__':
    main()
