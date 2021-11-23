from rest_framework import serializers
from authentication.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    This is a ModelSerializer for User Registration
    """

    class Meta:
        model = User
        fields = ('password', 'username', 'first_name', 'last_name', 'user_type')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    """
    This is a ModelSerializer for User Registration
    """

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    username = serializers.EmailField(required=True, allow_null=False, allow_blank=False)
    password = serializers.CharField(required=True, allow_null=False, allow_blank=False)
