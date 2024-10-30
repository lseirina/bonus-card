"""Tests for models."""
from django.contrib.auth.models import User
from django.utils import timezone
from django.test import TestCase

from core.models import BonusCard

from datetime import datetime


def create_user(username='Testuser', password='Test123'):
    """Create and return user."""
    return User.objects.create_user(
                username=username,
                password=password,
                )


class ModelTests(TestCase):
    """Test models."""

    def test_create_bonus_card(self):
        """Test create bonus card object."""
        user = create_user()
        bonus_card = BonusCard.objects.create(
            user=user,
            series='sdfgh',
            number='123ghjk',
            issue_date=timezone.now(),
            expiration_date=datetime(2024, 12, 20, 12, 30),
            balance=100.00,
        )

        self.assertIsNotNone(bonus_card.id)
        self.assertEqual(bonus_card.series, 'sdfgh')
        self.assertEqual(bonus_card.number, '123ghjk')

    def test_check_expiration(self):
        """Test checking expiration date."""
        user = create_user()
        bonus_card = BonusCard.objects.create(
            user=user,
            series='sdfgh',
            number='123ghjk',
            issue_date=timezone.now(),
            expiration_date=timezone.make_aware(datetime(2023, 7, 20, 12, 30)),
            balance=100.00,
            status='active',
        )
        bonus_card.check_expiration()

        bonus_card.refresh_from_db()
        self.assertEqual(bonus_card.status, 'expired')
