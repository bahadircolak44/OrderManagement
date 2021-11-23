from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.test_data import CATEGORIES, RESTAURANT, FOOD, user_data, user_data2


class EndpointTests(APITestCase):
    def setUp(self):
        self.client.post('/register/', user_data, format='json')
        response = self.client.post('/api-token-auth/', user_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data.get('token'))

    def test_register_user(self):
        response = self.client.post('/register/', user_data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data.get('id')

    def test_login_user(self):
        response = self.client.post('/api-token-auth/', user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data.get('token'))

    def test_category_create(self):
        # Category Create
        for category in CATEGORIES:
            response = self.client.post('/serve/category/', data=category, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_category_list(self):
        # Generate data
        self.test_category_create()

        response = self.client.get('/serve/category/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return [data.get('id') for data in response.data]

    def test_category_retrieve(self):
        # Get ID list of data
        category_id_list = self.test_category_list()
        for category_id in category_id_list:
            response = self.client.get(f'/serve/category/{category_id}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('id'), category_id)

    def test_restaurant_create(self):
        owner_id = self.test_register_user()
        # Restaurant Create
        for restaurant in RESTAURANT:
            restaurant['owner'] = owner_id
            response = self.client.post('/serve/restaurant/', data=restaurant, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_restaurant_list(self):
        # Generate data
        self.test_restaurant_create()
        response = self.client.get('/serve/restaurant/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return [data.get('id') for data in response.data]

    def test_restaurant_retrieve(self):
        # Get ID list of data
        restaurant_id_list = self.test_restaurant_list()
        for restaurant_id in restaurant_id_list:
            response = self.client.get(f'/serve/restaurant/{restaurant_id}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('id'), restaurant_id)

    def test_food_create(self):
        restaurant_id_list = self.test_restaurant_list()
        category_id_list = self.test_category_list()
        zipped_list = list(zip(restaurant_id_list, category_id_list))
        # Get ID list of data
        for index, food in enumerate(FOOD):
            if index < 3:
                food['restaurants'] = zipped_list[0][0]
                food['categories'] = zipped_list[0][1]
            elif index < 6:
                food['restaurants'] = zipped_list[1][0]
                food['categories'] = zipped_list[1][1]
            else:
                food['restaurants'] = zipped_list[2][0]
                food['categories'] = zipped_list[2][1]
            response = self.client.post('/serve/food/', data=food, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_food_list(self):
        # Generate data
        self.test_food_create()
        response = self.client.get('/serve/food/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return [data.get('id') for data in response.data]

    def test_food_retrieve(self):
        # Get ID list of data
        food_id_list = self.test_food_list()
        for food_id in food_id_list:
            response = self.client.get(f'/serve/food/{food_id}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('id'), food_id)

    # def test_order_create(self):
    #     food_id_list = self.test_food_list()
    #     # Get ID list of data
    #     for food_id in food_id_list:
    #         response = self.client.post('/serve/order/',
    #                                     data={'foods': food_id},
    #                                     format='json')
    #         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_order_list(self):
        # Generate data
        # self.test_order_create()
        response = self.client.get('/serve/order/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return [data.get('id') for data in response.data]

    def test_order_retrieve(self):
        # Get ID list of data
        order_id_list = self.test_order_list()
        for order_id in order_id_list:
            response = self.client.get(f'/serve/order/{order_id}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('id'), order_id)
