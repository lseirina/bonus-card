"""Views for Bonus card API."""
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from core.models import BonusCard
from core.serializers import BonusCardSerializer


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