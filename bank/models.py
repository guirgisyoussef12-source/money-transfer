from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Transaction(models.Model):
    sender = models.ForeignKey(
        UserProfile,
        related_name='sent_transactions',
        on_delete=models.CASCADE
    )

    receiver = models.ForeignKey(
        UserProfile,
        related_name='received_transactions',
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver} : {self.amount}"
