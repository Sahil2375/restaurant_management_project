from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from home.models import Restaurant

# Create your tests here.

class RestaurantInfoAPITest(APITestCase):

    def setUp(self):
        # Create a sample restaurant for testing
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            address='123 Test St'
        )

    def test_get_restaurant_info(self):
        """
        Ensure that the restaurant info API returns correct data.
        """
        # Send a GET request to the API endpoint
        response = self.client.get('/api/restaurant-info/')

        # Check if the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that the response contains the expected restaurant data
        self.assertIn('name', response.data)
        self.assertIn('address', response.data)
        self.assertEqual(response.data['name'], self.restaurant.name)
        self.assertEqual(response.data['address'], self.restaurant.address)
