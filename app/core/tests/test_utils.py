"""
Test for generate bonus_card method.
"""
from datetime import timedelta
from core.models import BonusCard
from core.utils import generate_cards

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model


def create_user(username='TestUser', password='Test123'):
    """Create and return user."""
    return get_user_model().objects.create(
        username=username,
        password=password,
    )


class GenerateCardsTest(TestCase):
    def test_geberate_cards_correct_count(self):
        """Test genereta correct count ob bonus cards."""
        user = create_user()
        series = 'TEST'
        count = 5
        expiration_period = '6_months'

        generate_cards(user, series, count, expiration_period)

        cards = BonusCard.objects.filter(series=series)

        self.assertEqual(cards.count(), count)

    def test_generate_cards_correct_expiration_period(self):
        """Test generate card correct expiration date."""
        user = create_user()
        series = 'TEST'
        count = 6
        expiration_period = '1_month'
        expected_expiration_date = timezone.now() + timedelta(days=30)

        generate_cards(user, series, count, expiration_period)
        cards = BonusCard.objects.filter(series=series)

        for card in cards:
            self.assertAlmostEqual(
                card.expiration_date,
                expected_expiration_date,
                delta=timedelta(seconds=1)
                )

    def test_generate_cards_unique_number(self):
        """Test generate cards with unique number."""
        user = create_user()
        series = 'UNIQUE'
        count = 4
        expiration_period = '6_months'

        generate_cards(user, series, count, expiration_period)

        numbers = BonusCard.objects.filter(series=series).values_list('number', flat=True)

        self.assertEqual(len(numbers), len(set(numbers)))