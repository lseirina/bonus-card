"""Tests for bomus card api."""
from datetime import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from core.models import BonusCard
from core.serializers import BonusCardSerializer

BONUS_CARDS_URL = reverse('card:card-list')


def detail_bonus_card(bonus_card_id):
    return reverse('card:card-detail', args=[bonus_card_id])


def create_user(**params):
    """create and return user."""
    return get_user_model().objects.create_user(**params)


def create_bonus_card(user, **params):
    """Create and return bonus card."""
    defaults = {
        'series': 'sdfgh',
        'number': '123ghjk',
        'issue_date': timezone.now(),
        'expiration_date': datetime(2024, 12, 20, 12, 30),
        'balance': 100.00,
    }
    defaults.update(params)

    bonus_card = BonusCard.objects.create(user=user, **defaults)

    return bonus_card