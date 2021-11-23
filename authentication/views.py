import traceback

from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from authentication.serializers import UserRegisterSerializer, UserLoginSerializer


class RegistrationView(APIView):
    """
    You can register the application using this view.
    It is very simple,
    No need to apply permission and authentication class because user has none.

    Method: [POST]
    Endpoint: /register/
    Example:
        {
            "username": "test@test.com",
            "password": "password",
            "first_name": "FirstName",
            "last_name": "LastName"
        }
    """
    permission_classes = []
    authentication_classes = []

    def post(self, *args, **kwargs):
        try:
            serializer = UserRegisterSerializer(data=self.request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(dict(id=serializer.instance.id), status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            print(traceback.format_exc())  # for error_log
            return Response(data=str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    """

    !!! NOT IN USED !! JUST FOR EXAMPLE

    You can login the application using this view.
    It is very simple,
    No need to apply permission and authentication class because user has none.

    Method: [POST]
    Endpoint: /api-token-auth/
    Example:
        {
            "username": "test@test.com",
            "password": "password"
        }
    """
    permission_classes = []
    authentication_classes = []

    def post(self, *args, **kwargs):
        try:
            serializer = UserLoginSerializer(data=self.request.data)
            if serializer.is_valid():
                user = authenticate(**serializer.validated_data)
                if user:
                    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)
                    login(self.request, user)
                    return Response(dict(token=token), status=status.HTTP_200_OK)
                return Response({"non_field_errors": ["Unable to log in with provided credentials."]},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            print(traceback.format_exc())  # for error_log
            return Response(data=str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(APIView):
    """
    You can logout the application using this view.
    Request need to contain valid token.

    Method: [POST]
    Endpoint: /logut/
    """

    def post(self, *args, **kwargs):
        try:
            user = self.request.user
            user.is_login = False
            user.save()
            logout(self.request)
            return Response()
        except Exception as ex:
            print(traceback.format_exc())  # for error_log
            return Response(data=str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
