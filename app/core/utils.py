"""
Method to generate bonus cards.
"""
import random
import string
from datetime import timedelta
from django.utils import timezone
from core.models import BonusCard


def generate_cards(series, count, expiration_period):
    expiration_map = {
        '1_year': timezone.now() + timedelta(days=365),
        '6_months': timezone.now() + timedelta(days=183),
        '1_month': timezone.now() + timedelta(days=30),
    }

    expiration_date = expiration_map.get(
        expiration_period, timezone.now() + timedelta(days=365)
        )

    for _ in range(count):
        BonusCard.objects.create(
            series=series,
            number=''.join(string.digits, k=16),
            expiration_date=expiration_date,
        )