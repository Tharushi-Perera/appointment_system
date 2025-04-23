import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import AppointmentForm
from .models import Appointment, Service
from .models import Service
from .models import ServiceSubCategory, Service
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def generate_time_slots(start_time, end_time, duration):
    slots = []
    current = start_time
    while current + datetime.timedelta(minutes=duration) <= end_time:
        slots.append(current.strftime("%H:%M"))
        current += datetime.timedelta(minutes=duration)
    return slots



def home(request):
    services = Service.objects.all()
    return render(request, 'home.html', {'listing_services': services})

#@login_required
# booking/views.py
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # Store service data in session
            request.session['appointment_data'] = {
                'service_id': form.cleaned_data['service'].id,
                'date': form.cleaned_data['date'].isoformat()
            }
            return redirect(reverse('booking:choose_time'))
    else:
        form = AppointmentForm()
    return render(request, 'booking/book.html', {'form': form})


#@login_required
# booking/views.py
def confirm_appointment(request):
    if request.method == 'POST':
        data = request.session.get('appointment_data')
        if data:
            quantity = int(request.POST.get('quantity', 1))
            service = Service.objects.get(id=data['service_id'])

            for _ in range(quantity):
                Appointment.objects.create(
                    user=request.user,
                    service=service,
                    date=data['date'],
                    time=request.POST.get('time'),
                    status='Pending'
                )
            return redirect('booking:my_appointments')
    return redirect('booking:book_appointment')


#@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(user=request.user).order_by('-date')
    return render(request, 'booking/my_appointments.html', {'appointments': appointments})

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = ServiceSubCategory.objects.filter(
        category_id=category_id
    ).order_by('display_order').values('id', 'name')
    return JsonResponse({
        'subcategories': list(subcategories)
    })

def get_services(request):
    subcategory_id = request.GET.get('subcategory_id')
    services = Service.objects.filter(
        subcategory_id=subcategory_id,
        available=True
    ).order_by('name').values('id', 'name', 'price', 'duration_minutes')
    return JsonResponse({
        'services': list(services)
    })


def choose_time(request):
    data = request.session.get('appointment_data')
    if not data:
        return redirect('booking:book_appointment')

    try:
        service = Service.objects.get(id=data['service_id'])
        date = datetime.date.fromisoformat(data['date'])

        # Generate time slots (9 AM to 5 PM)
        start_time = datetime.datetime.combine(date, datetime.time(9, 0))
        end_time = datetime.datetime.combine(date, datetime.time(17, 0))
        slots = generate_time_slots(start_time, end_time, service.duration_minutes)

        return render(request, 'booking/choose_time.html', {
            'service': service,
            'date': date,
            'slots': slots,
        })
    except (Service.DoesNotExist, KeyError, ValueError):
        return redirect('booking:book_appointment')

def add_to_cart(request):
    if request.method == 'POST':
        if 'cart' not in request.session:
            request.session['cart'] = []

        service_id = request.POST.get('service_id')
        date = request.POST.get('date')

        request.session['cart'].append({
            'service_id': service_id,
            'date': date
        })
        return JsonResponse({'status': 'success'})

def view_cart(request):
    cart = request.session.get('cart', [])
    services = []
    for item in cart:
        service = Service.objects.get(id=item['service_id'])
        services.append({
            'service': service,
            'date': item['date']
        })
    return render(request, 'booking/cart.html', {'services': services})