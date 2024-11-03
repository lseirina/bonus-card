"""Views for Bonus card API."""
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from django.filters import rest_framework as filters

from core.models import BonusCard
from core.serializers import BonusCardSerializer


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