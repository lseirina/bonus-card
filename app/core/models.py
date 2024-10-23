"""Database models."""
from django.db import models
from django.utils import timezone



class BonusCard(models.Model):
    """BonusCard object."""
    status_choices = [
        ('inactive', 'Не активирована'),
        ('active', 'Активирована'),
        ('expired', 'Просрочена')
    ]
    seria = models.CharField(max_length=10)
    number = models.CharField(max_length=16, unique=True)
    issue_date = models.DateTimeField(timezone.now())
    expiration_date = models.DateTimeField()
    last_used_date = models.DateTimeField(null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=10, choice=status_choices, default='inactive'
        )

    def check_expiration(self):
        """Check if card is expired."""
        if timezone.now > self.expiration_date:
            self.status = 'expired'
            self.save()

    def __str__(self):
        return f'{self.seria} {self.number} - {self.status}'
