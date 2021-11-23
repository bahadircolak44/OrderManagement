import traceback

from django.db import models
from rest_framework import status
from rest_framework.response import Response

from api.db_models.base import BaseModel
from api.db_models.food import Food
from utils.publish import publish


class Order(BaseModel):
    class Status(models.TextChoices):
        IDLE = 'I'
        RUNNING = 'R'
        QUEUED = 'Q'
        SUCCESS = 'S'
        FAILED = 'F'
        CANCELED = 'C'

    foods = models.ForeignKey(Food, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.IDLE)

    class Meta:
        db_table = 'db_order'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @classmethod
    def list_by_user(cls, serializer, user_id):
        """
        Later, another models want to consume message, so the method is generic.
        Just defined it in Model which is inherited BaseModel.
        In the views.py this method will be called by consume()
        """
        data_list = cls.objects.filter(foods__restaurants__owner_id=user_id)
        return Response(serializer(data_list, many=True).data, status=status.HTTP_200_OK)

    @classmethod
    def publish_message(cls, serializer, *, basename, user_id):
        try:
            restaurant = serializer.instance.foods.restaurants
            owner = restaurant.owner
            if owner.is_login:
                restaurants_id = restaurant.id
                publish({'id': serializer.instance.id}, f"{basename}-{restaurants_id}")
                serializer.instance.status = Order.Status.QUEUED
                serializer.save()
                return True
            else:
                serializer.instance.delete()
                return False
        except:
            # If there will be any problem, celery will handle
            print(traceback.format_exc())
            serializer.instance.status = Order.Status.IDLE
            serializer.save()
            return False

    @classmethod
    def complete(cls, serializer_class, data):
        """
        Later, another models want to consume message, so the method is generic.
        Just defined it in Model which is inherited BaseModel.
        In the views.py this method will be called by consume()
        """
        try:
            serializer = serializer_class(data=data)
            if serializer.is_valid():
                order = cls.objects.get(**serializer.validated_data)
                order.status = cls.Status.SUCCESS
                order.save()
                return Response(status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except cls.DoesNotExist:
            return Response('Order does not exists', status=status.HTTP_400_BAD_REQUEST)