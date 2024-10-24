"""Tests for models."""
from django.utils import timezone
from django.test import TestCase

from core.models import BonusCard

from datetime import datetime


class ModelTests(TestCase):
    """Test models."""

    def test_create_bonus_card(self):
        """Test create bonus card object."""
        bonus_card = BonusCard.objects.create(
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

        bonus_card = BonusCard.objects.create(
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
