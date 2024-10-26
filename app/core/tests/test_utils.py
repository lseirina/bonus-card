"""
Test for generate bonus_card method.
"""
from datetime import timedelta
from core.models import BonusCard
from core.utils import generate_cards

from django.test import TestCase
from django.utils import timezone


class GenerateCardsTest(TestCase):
    def test_geberate_bonus_card_correct_count(self):
        """Test genereta correct count ob bonus cards."""
        series = 'TEST',
        count = 5
        expiration_period = '6_months'

        generate_cards(series, count, expiration_period)

        cards = BonusCard.objects.filter(series=series)

        self.assertEqual(cards.count(), count)
