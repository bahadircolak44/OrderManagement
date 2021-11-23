import pytest
from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator

from OrderManagement.asgi import application

TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
class TestWebSocket:
    async def test_can_connect_to_server(self, settings, get_or_create_token):
        token = await sync_to_async(get_or_create_token)()
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/ws/order/1/?token={token}'
        )
        connected, _ = await communicator.connect()
        assert connected is True
        await communicator.disconnect()
