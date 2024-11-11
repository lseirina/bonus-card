from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


TOKEN_URL = reverse('card:token')


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
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_bad_credentials(self):
        """Test return error if creadentials invalid."""
        payload = {'username': '', 'password': 'badpass'}
        res =  self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)