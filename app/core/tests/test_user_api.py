from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import APIClient
from rest_framework.test import status


TOKEN_URL = reverse('token')


class TokenAPITest(TestCase):
    """Tests for token api."""
    def setUp(self):
        self.user = User.objects.create_user(
            username='Testname',
            password='test123'
        )
        self.client = APIClient()

    def test_create_token_for_user(self):
        """Test generate token for valid credentials"""
        user_details = {
            'username': 'Newname',
            'password': 'testpass123',
        }
        User.objects.create_user(**user_details)
        payload = {
            'username': user_details['username'],
            'password': user_details['password'],
        }
        