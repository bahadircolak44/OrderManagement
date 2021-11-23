"""
This file is useless now, but can be used for future.
It creates channel, thus restaurants and customer can send message each other
For example: Create Order
"""
import json
import threading

import pika
from channels.generic.websocket import JsonWebsocketConsumer
from django.conf import settings


# @database_sync_to_async
def change_order_status(**kwargs):
    from api.db_models.order import Order
    Order.objects.filter(**kwargs).update(status=Order.Status.RUNNING)


# @database_sync_to_async
def change_order_status(**kwargs):
    from api.db_models.order import Order
    Order.objects.filter(**kwargs).update(status=Order.Status.RUNNING)


class OrderConsumer(JsonWebsocketConsumer):
    """
    SyncConsumer that handles connection of orders.
    """

    def callback(self, ch, method, properties, body):
        order_id = json.loads(body.decode()).get("id")
        if order_id:
            message = f'A new order has received >>> Order : {order_id}'
            change_order_status(id=order_id)
            self.send_json(message)

    def connect(self):
        user = self.scope['user']
        if user.is_authenticated:
            user.is_login = True
            user.save()
            restaurant_id = self.scope['url_route']['kwargs'].get('restaurant_id', None)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
            channel = connection.channel()
            self.queue_connection = connection
            channel.exchange_declare(exchange=f'order-{restaurant_id}', exchange_type='fanout')
            # let the server choose a random queue name for us.
            # once the consumer connection is closed, the queue should be deleted. exclusive flag is for that
            result = channel.queue_declare(queue='', exclusive=True)
            queue_name = result.method.queue

            channel.queue_bind(exchange=f'order-{restaurant_id}', queue=queue_name)

            channel.basic_consume(
                queue=queue_name, on_message_callback=self.callback, auto_ack=True)

            self.group_name = f'order-{restaurant_id}'
            self.accept()
            self.channel_layer.group_add(self.group_name, self.channel_name)
            self.th = threading.Thread(target=channel.start_consuming, daemon=True)
            self.th.start()
            return
        else:
            self.close()

    def disconnect(self, code):
        user = self.scope['user']
        user.is_login = False
        user.save()

        self.channel_layer.group_discard(self.group_name, self.channel_name)
        self.close()
        self.queue_connection.close()