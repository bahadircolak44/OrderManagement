from django.db import models
from rest_framework import status
from rest_framework.response import Response


class BaseModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @classmethod
    def list_by_user(cls, serializer, user_id):
        """
        Later, another models want to consume message, so the method is generic.
        Just defined it in Model which is inherited BaseModel.
        In the views.py this method will be called by consume()
        """
        return Response({
            "detail": "Not found."
        }, status=status.HTTP_404_NOT_FOUND)

    @classmethod
    def consume_message(cls, serializer, channel_name):
        """
        Later, another models want to consume message, so the method is generic.
        Just defined it in Model which is inherited BaseModel.
        In the views.py this method will be called by consume()
        """
        return Response({
            "detail": "Not found."
        }, status=status.HTTP_404_NOT_FOUND)

    @classmethod
    def publish_message(cls, serializer, *, basename, user_id):
        """
        Later, another models want to publish message, so the method is generic.
        Just defined it in Model which is inherited BaseModel.
        In the views.py this method will be called by perform_create()
        """
        return True

    @classmethod
    def complete(cls, serializer_class, data):
        """
        Later, another models want to consume message, so the method is generic.
        Just defined it in Model which is inherited BaseModel.
        In the views.py this method will be called by consume()
        """
        return Response({
            "detail": "Not found."
        }, status=status.HTTP_404_NOT_FOUND)
