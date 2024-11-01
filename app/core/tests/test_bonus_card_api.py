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


class PublicBonusCardAPITests(TestCase):
    """Tests unauthenticated API requests."""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication required for request."""
        res = self.client.get(BONUS_CARDS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBonusCardAPITest(TestCase):
    """Tests for authorized user."""
    def setUp(self):
        self.user = create_user(
            username='TestName',
            password='Test123',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_list(self):
        """Test retrieve list of bonus cards."""
        create_bonus_card(user=self.user, number='kjhgf67')
        create_bonus_card(user=self.user)

        res = self.client.get(BONUS_CARDS_URL)
        cards = BonusCard.objects.all()
        serializer = BonusCardSerializer(cards, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_card_limit_to_user(self):
        """Test retrieving cards are limited to authenticated user."""
        other_user = create_user(username='OtherUser', password='Testpass123')

        create_bonus_card(user=self.user)
        create_bonus_card(user=other_user, number='gklk90')

        card = BonusCard.objects.filter(user=self.user)
        serializer = BonusCardSerializer(card, many=True)
        res = self.client.get(BONUS_CARDS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_card(self):
        """Test create card success."""
        payload = {
            'series': 'sdfgh',
            'number': '123ghjk',
            'issue_date': timezone.now(),
            'expiration_date': datetime(2024, 12, 20, 12, 30),
            'balance': 100.00,
        }
        res = self.client.post(BONUS_CARDS_URL, payload)

        self.assertEqaul(res.status_code, status.HTTP_201_CREATED)
        card = BonusCard.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(card, k), v)
        self.assertEqual(res.user, self.user)
