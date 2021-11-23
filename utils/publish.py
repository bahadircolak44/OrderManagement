import json
import pika
from django.conf import settings


def publish(json_data, channel_name):
    """
    This function send message to the rabbitmq pubsub mechanism

    :param json_data: message that will send to queue
    :param channel_name: which channel message will be sent
    :return: None
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange=channel_name, exchange_type='fanout')
    channel.basic_publish(exchange=channel_name, routing_key='', body=json.dumps(json_data).encode())
    connection.close()
