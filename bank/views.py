from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from decimal import Decimal

from .models import UserProfile, Transaction


# =========================
# Helper
# =========================
def get_user_profile(user):
    return get_object_or_404(UserProfile, user=user)


# =========================
# Dashboard
# =========================
@login_required
def dashboard_view(request):

    profile = get_user_profile(request.user)

    return render(request, "dashboard.html", {
        "profile": profile
    })


# =========================
# Add Money
# =========================
@login_required
def add_money(request):

    profile = get_user_profile(request.user)

    if request.method == "POST":

        amount = request.POST.get("amount")

        try:
            amount = Decimal(amount)
        except:
            return render(request, "add_money.html", {
                "balance": profile.balance,
                "error": "Invalid amount"
            })

        if amount <= 0:
            return render(request, "add_money.html", {
                "balance": profile.balance,
                "error": "Amount must be greater than 0"
            })

        with transaction.atomic():
            profile.balance += amount
            profile.save()

        return redirect("dashboard")

    return render(request, "add_money.html", {
        "balance": profile.balance
    })


# =========================
# Transfer Money
# =========================
@login_required
def transfer_view(request):

    sender = get_user_profile(request.user)

    if request.method == "POST":

        receiver_username = request.POST.get("receiver")
        amount = request.POST.get("amount")

        try:
            amount = Decimal(amount)
        except:
            return render(request, "transfer.html", {
                "error": "Invalid amount"
            })

        if amount <= 0:
            return render(request, "transfer.html", {
                "error": "Amount must be greater than 0"
            })

        receiver = UserProfile.objects.filter(
            user__username=receiver_username
        ).first()

        if not receiver:
            return render(request, "transfer.html", {
                "error": "Receiver not found"
            })

        if receiver.user == request.user:
            return render(request, "transfer.html", {
                "error": "You cannot transfer to yourself"
            })

        if sender.balance < amount:
            return render(request, "transfer.html", {
                "error": "Insufficient balance"
            })

        with transaction.atomic():

            sender.balance -= amount
            receiver.balance += amount

            sender.save()
            receiver.save()

            Transaction.objects.create(
                sender=sender,
                receiver=receiver,
                amount=amount
            )

        return redirect("dashboard")

    return render(request, "transfer.html")


# =========================
# Transaction History
# =========================
@login_required
def transaction_history(request):

    profile = get_user_profile(request.user)

    sent = Transaction.objects.filter(sender=profile)
    received = Transaction.objects.filter(receiver=profile)

    transactions = sent.union(received).order_by("-timestamp")

    return render(request, "history.html", {
        "transactions": transactions
    })