"""
Serializers for BonusCard API.
"""
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

from core.models import BonusCard


class UserSerializer(serializers.ModelSerialiser):
    """Serializer for user object."""
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

        def creat(self, validated_data):
            """Create and return user with token."""
            user = User.objects.create_user(**validated_data)
            Token.objects.create(user=user)
            return user


class BonusCardSerializer(serializers.ModelSerializer):
    """Serializer for bonus cards."""
    class Meta:
        model = BonusCard
        fields = [
            'id', 'series', 'number', 'expiration_date', 'status', 'balance'
            ]
        read_only_fields = ['id']
