from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_backends
from .forms import SignUpForm, ProfileUpdateForm, UserForm, UserProfileForm
from booking.models import Appointment
from accounts.models import UserProfile
from collections import Counter


def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create UserProfile ONLY IF it doesn't already exist
            UserProfile.objects.get_or_create(user=user)

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('accounts:profile')
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
    return redirect('home')

@login_required
def profile_view(request):
    user = request.user

    # Ensure the profile exists
    profile, created = UserProfile.objects.get_or_create(user=user)

    # Fetch appointments
    past_appointments = Appointment.objects.filter(user=user, date__lt=timezone.now()).order_by('-date')
    upcoming_appointments = Appointment.objects.filter(user=user, date__gte=timezone.now()).order_by('date')

    # Analyze usage
    freq_services = Counter([a.service.name for a in past_appointments])
    freq_stylists = Counter([a.service.subcategory.name for a in past_appointments if a.service.subcategory])  # or a.stylist.name if stylist exists

    return render(request, 'accounts/profile.html', {
        'user': user,
        'profile': profile,
        'past_appointments': past_appointments,
        'upcoming_appointments': upcoming_appointments,
        'freq_services': dict(freq_services),
        'freq_stylists': dict(freq_stylists),
    })


@login_required
def profile_edit(request):
    user_form = UserForm(instance=request.user)
    profile_form = UserProfileForm(instance=request.user.userprofile)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('accounts:profile')

    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  # Log out before deletion
        user.delete()
        return redirect('home')  # Redirect to home after deletion