from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from social_network.models import User

class UserTests(APITestCase):
    def test_create_user_profile(self):
        """
        Ensure we can create a new user object.
        """
        url = '/users/'
        user_data = {
            "img": "https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500",
            "first_name": "Steph",
            "last_name": "Walters",
            "phone": "(820) 289-1818",
            "address": "5190 Center Court Drive",
            "city": "Spring",
            "state": "TX",
            "zipcode": "77370",
            "available": True
            }
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().first_name, 'Steph')