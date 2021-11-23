import traceback
from urllib import parse

import jwt
from asgiref.sync import sync_to_async
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections

from api.db_models.order import Order
from authentication.models import User


class TokenError(Exception):
    pass


@database_sync_to_async
def get_order(**kwargs):
    try:
        return User.objects.filter(**kwargs)
    except Order.DoesNotExist:
        return None


@database_sync_to_async
def get_user(**kwargs):
    try:
        return User.objects.get(**kwargs)
    except User.DoesNotExist:
        return AnonymousUser()


class JwtAuthMiddleware:

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        try:
            self.scope = scope
            await sync_to_async(close_old_connections)()
            if self.scope.get('user') and self.scope.get('user').is_active:
                return await self.app(dict(self.scope, user=self.scope.get('user')), receive, send)
            query_string = self.scope["query_string"]
            if not query_string:
                raise TokenError()

            query_dict = parse.parse_qs(query_string.decode('utf-8'))
            raw_token = query_dict['token'][0]
            decoded_token = jwt.decode(raw_token, settings.SECRET_KEY, algorithms=["HS256"])
            user = await get_user(username=decoded_token.get('username'))
            return await self.app(dict(self.scope, user=user), receive, send)

        except Exception as exc:
            print(traceback.format_exc())
            return await self.app(dict(self.scope, user=AnonymousUser()), receive, send)


JwtAuthMiddlewareStack = lambda app: JwtAuthMiddleware(AuthMiddlewareStack(app))
