"""Tests for models."""
from django.utils import timezone
from django.test import TestCase
from core.models import BonusCard


class ModelTests(TestCase):
    """Test models."""

    bonus_card = BonusCard.objects.create(
        seria='sdfgh',
        number='123ghjk',
        issue_date=timezone.now(),
        expiration_date=
    )
