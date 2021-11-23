import traceback

from django.db import models
from api.db_models.base import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'db_category'

    @classmethod
    def generate_initial(cls):
        try:
            category_list = ['Döner/Kebap', 'Ev Yemekleri', 'Fast-Food']
            cls.objects.bulk_create([cls(name=name) for name in category_list])
            return True
        except Exception as ex:
            print(traceback.format_exc())
            return False
