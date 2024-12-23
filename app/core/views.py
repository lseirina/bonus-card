"""Views for Bonus card API."""
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend

from core.models import BonusCard
from core.serializers import (
    BonusCardSerializer,
    UserSerializer,
    CustomAuthTokenSerializer,
    )


class CreateUserView(generics.CreateAPIView):
    """Create a new user in asystem."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = CustomAuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class BonusCardFilter(filters.FilterSet):
    """Filter class."""
    issue_date = filters.DateFromToRangeFilter()
    expiration_date = filters.DateFromToRangeFilter()

    class Meta:
        model = BonusCard
        fields = [
            'series', 'number', 'status', 'issue_date', 'expiration_date'
            ]


class BonusCardViewSet(viewsets.ModelViewSet):
    """View for bonus cards."""
    queryset = BonusCard.objects.all()
    serializer_class = BonusCardSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BonusCardFilter

    def perform_update(self, serializer):
        """Check the expiration date when update."""
        instance = serializer.save()
        instance.check_expiration()

    def get_queryset(self):
        """Return bonus cards for the authenticated user only."""
        return BonusCard.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new user."""
        serializer.save(user=self.request.user)
