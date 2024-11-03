"""
Serializers for BonusCard API.
"""
from rest_framework import serializers

from core.models import BonusCard


class BonusCardSerializer(serializers.ModelSerializer):
    """Serializer fot bonus cards."""
    class Meta:
        model = BonusCard
        fields = [
            'id', 'series', 'number', 'expiration_date', 'status', 'balance'
            ]
        read_only_fields = ['id']
