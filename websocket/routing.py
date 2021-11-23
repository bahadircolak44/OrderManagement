from django.conf.urls import url

from websocket.consumers import OrderConsumer

websocket_urlpatterns = [
    url(r"^ws/order/(?P<restaurant_id>[0-9]+)/$", OrderConsumer.as_asgi()),
]
