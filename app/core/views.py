"""Views for Bonus card API."""
from rest_framework import viewsets
from core.models import BonusCard
from core.serializers import BonusCardSerializer


class BonusCardViewSet(viewsets.ModelViewSet):
    """View for bonus cards."""
    queryset = BonusCard.objects.all()
    serializer = BonusCardSerializer

    def perform_update(self, serializer):
        """Check the expiration date when update."""
        instance = serializer.save()
        instance.check_expiration()
