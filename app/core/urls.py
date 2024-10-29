"""Urls mapping for BonusCard app."""
from django.urls import (
    path,
    include
    )
from rest_framework.routers import DefaultRouter
from core.views import BonusCardViewSet

router = DefaultRouter()
router.register('cards', BonusCardViewSet, basename='card')

app_name = 'card'

urlpatterns = [
    path('', include(router.urls))
]