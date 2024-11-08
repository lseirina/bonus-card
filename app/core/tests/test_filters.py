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
            issue_date=timezone.now() - timedelta(days=5),
            expiration_date=timezone.make_aware(
                datetime(2024, 11, 5, 12, 30)
                ),
            balance=Decimal(100.00),
            status='expired'
        )

        self.cards2 = BonusCard.objects.create(
            user=self.user,
            series='wertyui',
            number='1232345',
            issue_date=timezone.now() - timedelta(days=30),
            expiration_date=timezone.make_aware(
                datetime(2024, 12, 20, 12, 30)
                ),
            balance=Decimal(100.00),
            status='active',
        )

    def test_filter_series(self):
        """Test filtering bonus card by series."""
        res = self.client.get(URL_BONUS_CARD, {'series': 'sdfgh'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['series'], 'sdfgh')

    def test_filter_status(self):
        """Test filtering bonus cards by status."""
        res = self.client.get(URL_BONUS_CARD, {'status': 'active'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['status'], 'active')

    def test_filter_number(self):
        """Test filtering cards by number."""
        res = self.client.get(URL_BONUS_CARD, {'number': '1232345'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['number'], '1232345')

    def test_filter_issue_date(self):
        """Test filtering cards by issue date."""
        start_date = (timezone.now() - timedelta(days=10)).date()
        end_date = timezone.now().date()

        res = self.client.get(URL_BONUS_CARD, {
            'issue_date_after': start_date, 'issue_date_before': end_date}
                              )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['number'], '1237890')

    def test_filter_expiration_date(self):
        """Test filtering cards by expiration date."""
        start_date = (timezone.now() - timedelta(days=365)).date()
        end_date = timezone.now().date()

        res = self.client.get(URL_BONUS_CARD, {
            'expiration_date_after': start_date,
            'expiration_date_before': end_date
            }
                              )

        print(res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['number'], '1237890')