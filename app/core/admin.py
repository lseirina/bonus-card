"""Django admin customization."""
from django.contrib import admin

from core import models


class BonusCardAdmin(admin.ModelAdmin):
    """Define pages for bonuscasd admin."""
    search_fields = ['series', 'number', 'status']
    list_filter = ['status']


admin.site.register(models.BonusCard, BonusCardAdmin)
