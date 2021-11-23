"""
This is where you can manage services, url, serializer fields etc.
It very very important file
If you want to add new endpoint for a particular db (for example Restaurants)
Need to defined here.

!! NOTE !!: This file is just for Create, List and Retrieve services.

This file is read by api/urls.py and api/views.py

"""
from rest_framework import serializers

FOOD = {
    "url": "food",
    "db": "Food",
    "PERMISSIONS": {},
    "FIELD_LIST": ("id", "name", "categories", "restaurants")
}

CATEGORY = {
    "url": "category",
    "db": "Category",
    "PERMISSIONS": {},
    "FIELD_LIST": ("id", "name")
}

RESTAURANT = {
    "url": "restaurant",
    "db": "Restaurant",
    "PERMISSIONS": {},
    "FIELD_LIST": ("id", "name", "owner")
}

ORDER = {
    "url": "order",
    "db": "Order",
    "PERMISSIONS": {},
    "FIELD_LIST": ("id", "foods", "status"),
    "READ_ONLY_FIELD_LIST": ("restaurant", "category", "name", "status"),
    "EXTRA_FIELDS": {"name": serializers.CharField(source="foods.name", required=False),
                     "restaurant": serializers.CharField(source="foods.restaurants.name", required=False),
                     "category": serializers.CharField(source="foods.categories.name", required=False)}
}
