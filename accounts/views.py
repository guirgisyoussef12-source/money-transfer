from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

from .forms import SignUpForm
from bank.models import UserProfile


def sign_up(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():

            user = form.save()

            UserProfile.objects.create(user=user)

            login(request, user)

            return redirect('dashboard')

    else:
        form = SignUpForm()

    return render(request, 'sign_up.html', {
        'form': form
    })


def login_view(request):

    if request.method == 'POST':

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            return redirect('dashboard')

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {
        'form': form
    })


def logout_view(request):

    logout(request)

    return redirect('login')