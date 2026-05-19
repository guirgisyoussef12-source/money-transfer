from django.shortcuts import render
from .models import UserProfile, Transaction




def dashboard_view(request):

    profile = UserProfile.objects.first()

    if not profile:

        return render(request, 'dashboard.html', {
            'error': 'No users found'
        })

    transactions = Transaction.objects.filter(
        sender=profile
    ) | Transaction.objects.filter(
        receiver=profile
    )

    transactions = transactions.order_by('-timestamp')

    context = {
        'profile': profile,
        'transactions': transactions,
    }

    return render(request, 'dashboard.html', context)
