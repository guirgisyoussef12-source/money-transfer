from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from .models import UserProfile, Transaction

def home(request):
    return render(request, 'home.html')




def dashboard_view(request):

    profile = request.user.userprofile

    transactions = Transaction.objects.filter(
        sender=profile
    ) | Transaction.objects.filter(
        receiver=profile
    )

    transactions = transactions.order_by('-timestamp')

    context = {
        'profile': profile,
        'transactions': transactions
    }

    return render(request, 'dashboard.html', context)