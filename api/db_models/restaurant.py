import traceback

from django.db import models
from rest_framework import status
from rest_framework.response import Response

from api.db_models.base import BaseModel
from authentication.models import User


class Restaurant(BaseModel):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'db_restaurant'

    @classmethod
    def generate_initial(cls):
        try:
            restaurant_list = [{'name': 'Süper Dönerci', 'owner_id': 1},
                               {'name': 'Harika Ev Yemekleri', 'owner_id': 2},
                               {'name': 'Bizim Büfe', 'owner_id': 3}]
            cls.objects.bulk_create([cls(**restaurant) for restaurant in restaurant_list])
            return True
        except Exception as ex:
            print(traceback.format_exc())
            return False

    @classmethod
    def list_by_user(cls, serializer, user_id):
        """
        Later, another models want to consume message, so the method is generic.
        Just defined it in Model which is inherited BaseModel.
        In the views.py this method will be called by consume()
        """
        data_list = cls.objects.filter(owner_id=user_id)
        return Response(serializer(data_list, many=True).data, status=status.HTTP_200_OK)