from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class JWTAuthTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.token_url = reverse("token_obtain_pair")

    def test_jwt_token_generation(self):
        response = self.client.post(
            self.token_url,
            {
                "username": "testuser",
                "password": "testpassword"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
