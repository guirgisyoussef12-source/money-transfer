from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
class Transaction(models.Model):

    class Status(models.TextChoices):
        SUCCESS = 'success'
        FAILED = 'failed'
        PENDING = 'pending'

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

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.SUCCESS
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} → {self.receiver} : {self.amount}"


