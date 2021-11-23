import traceback

from django.db import models
from rest_framework import status
from rest_framework.response import Response

from api.db_models.base import BaseModel
from api.db_models.category import Category
from api.db_models.restaurant import Restaurant


class Food(BaseModel):
    name = models.CharField(max_length=200)

    restaurants = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'db_food'

    @classmethod
    def generate_initial(cls):
        try:
            food_list = [
                {"name": "Döner", "restaurants_id": 1, "categories_id": 1},
                {"name": "İskender", "restaurants_id": 1, "categories_id": 1},
                {"name": "Etibol İskender", "restaurants_id": 1, "categories_id": 1},
                {"name": "Kuru Fasülye", "restaurants_id": 2, "categories_id": 2},
                {"name": "Pilav", "restaurants_id": 2, "categories_id": 2},
                {"name": "Mercibek Çorbası", "restaurants_id": 2, "categories_id": 2},
                {"name": "Goralı", "restaurants_id": 3, "categories_id": 3},
                {"name": "Dilli Kaşarlı", "restaurants_id": 3, "categories_id": 3},
                {"name": "Yengen", "restaurants_id": 3, "categories_id": 3},
            ]
            cls.objects.bulk_create([cls(**food) for food in food_list])
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
        data_list = cls.objects.filter(restaurants__owner_id=user_id)
        return Response(serializer(data_list, many=True).data, status=status.HTTP_200_OK)
