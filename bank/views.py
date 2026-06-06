from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from decimal import Decimal, InvalidOperation

from .models import UserProfile, Transaction


def get_user_profile(user):
    profile, created = UserProfile.objects.get_or_create(user=user)
    return profile


@login_required
def dashboard_view(request):
    profile = get_user_profile(request.user)

    recent_transactions = (
        Transaction.objects.filter(sender=profile) |
        Transaction.objects.filter(receiver=profile)
    ).order_by('-created_at')[:5]

    return render(request, 'dashboard.html', {
        'profile': profile,
        'recent_transactions': recent_transactions,
    })


@login_required
def add_money(request):
    profile = get_user_profile(request.user)

    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount', '0'))
        except InvalidOperation:
            return render(request, 'add_money.html', {
                'balance': profile.balance,
                'error': 'Invalid amount entered.'
            })

        if amount <= 0:
            return render(request, 'add_money.html', {
                'balance': profile.balance,
                'error': 'Amount must be greater than 0.'
            })

        with transaction.atomic():
            profile.balance += amount
            profile.save()

        return redirect('dashboard')

    return render(request, 'add_money.html', {
        'balance': profile.balance
    })


@login_required
def transfer_view(request):
    sender = get_user_profile(request.user)

    if request.method == 'POST':
        receiver_username = request.POST.get('receiver', '').strip()

        try:
            amount = Decimal(request.POST.get('amount', '0'))
        except InvalidOperation:
            return render(request, 'transfer.html', {
                'error': 'Invalid amount entered.',
                'sender': sender,
            })

        if amount <= 0:
            return render(request, 'transfer.html', {
                'error': 'Amount must be greater than 0.',
                'sender': sender,
            })

        receiver = UserProfile.objects.filter(
            user__username=receiver_username
        ).first()

        if not receiver:
            return render(request, 'transfer.html', {
                'error': f'User "{receiver_username}" not found.',
                'sender': sender,
            })

        if receiver.user == request.user:
            return render(request, 'transfer.html', {
                'error': 'You cannot transfer money to yourself.',
                'sender': sender,
            })

        if sender.balance < amount:
            return render(request, 'transfer.html', {
                'error': f'Insufficient balance. You have ${sender.balance}.',
                'sender': sender,
            })

        with transaction.atomic():
            sender.balance -= amount
            receiver.balance += amount
            sender.save()
            receiver.save()

            Transaction.objects.create(
                sender=sender,
                receiver=receiver,
                amount=amount,
                status=Transaction.Status.SUCCESS,
            )

        return redirect('dashboard')

    return render(request, 'transfer.html', {
        'sender': sender
    })


@login_required
def transaction_history(request):
    profile = get_user_profile(request.user)

    transactions = (
        Transaction.objects.filter(sender=profile) |
        Transaction.objects.filter(receiver=profile)
    ).order_by('-created_at')

    return render(request, 'history.html', {
        'transactions': transactions,
        'profile': profile,
    })