"""Tests filtering for bonus cards."""
from datetime import datetime, timedelta
from decimal import Decimal

from rest_framework.test import APIClient
from rest_framework import status

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from core.models import BonusCard


URL_BONUS_CARD = reverse('card:card-list')


class BonuscardFilterTest(TestCase):
    """Test filtering."""
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='TestName',
            password='Testpass123',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        self.cards1 = BonusCard.objects.create(
            user=self.user,
            series='sdfgh',
            number='1237890',
            issue_date=timezone.now(),
            expiration_date=timezone.make_aware(
                datetime(2024, 12, 20, 12, 30)
                ),
            balance=Decimal(100.00)
        )

        self.cards2 = BonusCard.objects.create(
            user=self.user,
            series='wertyui',
            number='1232345',
            issue_date=timezone.now(),
            expiration_date=timezone.make_aware(
                datetime(2024, 12, 20, 12, 30)
                ),
            balance=Decimal(100.00)
        )

    def test_filter_series(self):
        """Test filtering bonus card by series."""
        res = self.client.get(URL_BONUS_CARD, {'series': 'sdfgh'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['series'], 'sdfgh')
