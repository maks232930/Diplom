from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from barbershop.models import Master, Recording
from users.forms import LoginForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('barbershop:home')

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('barbershop:home')

    context = {
        'form': form,
    }

    return render(request, 'users/login.html', context)


@login_required
def profile_view(request):
    master = Master.objects.filter(user=request.user).first()

    if master is not None:
        recordings = Recording.objects.filter(date_and_time_of_recording__master=master)

        context = {
            'recordings': set(recordings),
        }

    else:
        context = {}

    return render(request, 'users/profile.html', context)


def user_logout(request):
    logout(request)
    return redirect('barbershop:home')
