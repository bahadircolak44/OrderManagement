import factory

from authentication.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'john{n}')
    email = factory.Sequence(lambda n: f'lennon{n}@thebeatles.com')
    password = factory.PostGenerationMethodCall('set_password', 'johnpassword')
