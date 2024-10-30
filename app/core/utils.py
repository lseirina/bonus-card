"""
Method to generate bonus cards.
"""
import random
import string
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from core.models import BonusCard


def generate_cards(user, series, count, expiration_period):
    expiration_map = {
        '1_year': timezone.now() + timedelta(days=365),
        '6_months': timezone.now() + timedelta(days=183),
        '1_month': timezone.now() + timedelta(days=30),
    }
    user = get_user_model().objects.create(
        username='CommandUser',
        password='Pass123'
    )
    expiration_date = expiration_map.get(
        expiration_period, timezone.now() + timedelta(days=365)
        )

    for _ in range(count):
        BonusCard.objects.create(
            user=user,
            series=series,
            number=''.join(random.choices(string.digits, k=16)),
            expiration_date=expiration_date,
        )
