import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from websocket.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OrderManagement.settings')

django_asgi_application = get_asgi_application()

from websocket.json_token_auth import JwtAuthMiddleware

application = ProtocolTypeRouter({
    "websocket": JwtAuthMiddleware(
        URLRouter(
            websocket_urlpatterns
        )
    )
})
