from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, ProfileUpdateForm
from booking.models import Appointment



def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sign-up successful! You can now log in.')
            return redirect('login')
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


@login_required
def profile_view(request):
    user = request.user
    past_appointments = Appointment.objects.filter(user=user, date__lt=timezone.now()).order_by('-date')
    upcoming_appointments = Appointment.objects.filter(user=user, date__gte=timezone.now()).order_by('date')

    services = [a.service.name for a in past_appointments]
    stylists = [a.service.subcategory.name for a in past_appointments]

    freq_services = {s: services.count(s) for s in set(services)}
    freq_stylists = {s: stylists.count(s) for s in set(stylists)}

    return render(request, 'accounts/profile.html', {
        'user': user,
        'past_appointments': past_appointments,
        'upcoming_appointments': upcoming_appointments,
        'freq_services': freq_services,
        'freq_stylists': freq_stylists,
    })


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})

