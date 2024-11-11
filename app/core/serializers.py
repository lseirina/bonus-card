"""
Serializers for BonusCard API.
"""
from rest_framework import serializers

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from core.models import BonusCard


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user object."""
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

        def creat(self, validated_data):
            """Create and return user with token."""
            user = User.objects.create_user(**validated_data)
            return user


class CustomAuthTokenSerializer(serializers.Serializer):
    """Serializer for user authtoken."""
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        username = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password,
        )
        if not user:
            msg = 'Unable to authenticate with provided credentials'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class BonusCardSerializer(serializers.ModelSerializer):
    """Serializer for bonus cards."""
    class Meta:
        model = BonusCard
        fields = [
            'id', 'series', 'number', 'expiration_date', 'status', 'balance'
            ]
        read_only_fields = ['id']
