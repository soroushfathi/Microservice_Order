import pika, json
from config.env import env

# params = pika.URLParameters(env('RABBITMQ_URL'))

#connection = pika.BlockingConnection(params)

# channel = connection.channel()

def publish(method, body):
    properties = piks.BasicProperties(method)
    channel.basic_publish(
        exchange='',
        routing_key='order.product',
        body=json.dumps(body),
        properties=properties
    )

