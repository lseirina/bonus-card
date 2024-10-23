"""Tests for models."""
from django.utils import timezone
from django.test import TestCase

from core.models import BonusCard

from datetime import datetime


class ModelTests(TestCase):
    """Test models."""

    def test_create_bonus_card(self):
        bonus_card = BonusCard.objects.create(
            seria='sdfgh',
            number='123ghjk',
            issue_date=timezone.now(),
            expiration_date=datetime(2024, 12, 20, 12, 30),
            balance=100.00,
        )

        self.asserIsNotNone(bonus_card.id)
        self.assertEqual(bonus_card.seria, 'sdfgh')
        self.assertEqual(bonus_card.number, '123ghjk')

        
