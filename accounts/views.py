from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from booking.models import Appointment


def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')

    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})

def home(request):
    return render(request, 'home.html')  # Correct path, Django looks inside templates/

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember_me')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if remember:
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)  # session ends when browser closes
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out.")
    return redirect('login')


@login_required
def profile_view(request):
    user = request.user
    past_appointments = user.appointments.filter(date__lt=timezone.now()).order_by('-date')
    upcoming_appointments = user.appointments.filter(date__gte=timezone.now()).order_by('date')

    return render(request, 'accounts/profile.html', {
        'user': user,
        'past_appointments': past_appointments,
        'upcoming_appointments': upcoming_appointments,
    })
