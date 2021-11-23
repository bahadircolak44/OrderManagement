import requests
from pytest_factoryboy import register

import pytest
from websocket.tests.factories import UserFactory

register(UserFactory)  # name of fixture is user_factory


@pytest.fixture
def test_password():
    return 'strong-test-pass'


# Use user_factory instead of create_user.
@pytest.fixture
def create_user(db, user_factory, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return user_factory(**kwargs)

    return make_user


# For Token Based Login
@pytest.fixture
def get_or_create_token(db, user_factory):
    def create_token(**kwargs):
        data = {
            'username': 'test@test.com',
            'password': '123456'
        }
        response = requests.post('http://localhost:8080/register/', data=data)
        user = None
        if response.status_code == 200:
            token = response.json()["token"]
            return token

    return create_token
