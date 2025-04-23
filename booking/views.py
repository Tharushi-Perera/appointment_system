import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import AppointmentForm
from .models import Appointment, Service
from .models import Service
from .models import ServiceSubCategory, Service
from django.contrib.auth.decorators import login_required


def generate_time_slots(start_time, end_time, duration):
    slots = []
    current = start_time
    while current + datetime.timedelta(minutes=duration) <= end_time:
        slots.append(current.strftime("%H:%M"))
        current += datetime.timedelta(minutes=duration)
    return slots

def load_services(request):
    category_id = request.GET.get('category')
    services = Service.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(services), safe=False)

def home(request):
    services = Service.objects.all()
    return render(request, 'home.html', {'listing_services': services})

#@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # Save data to session
            request.session['appointment_data'] = {
                'service_id': form.cleaned_data['service'].id,
                'date': form.cleaned_data['date'].isoformat()
            }
            return redirect('confirm_appointment')
    else:
        form = AppointmentForm()

    return render(request, 'booking/book.html', {'form': form})


#@login_required
def confirm_appointment(request):
    if request.method == 'POST':
        data = request.session.get('appointment_data')
        if data:
            service = Service.objects.get(id=data['service_id'])
            appointment = Appointment.objects.create(
                user=request.user,
                service=service,
                date=data['date'],
                time=request.POST.get('time'),
                status='Pending'
            )
            return redirect('my_appointments')
    return redirect('book_appointment')


#@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(user=request.user).order_by('-date')
    return render(request, 'booking/my_appointments.html', {'appointments': appointments})

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = ServiceSubCategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse({'subcategories': list(subcategories)})

def get_services(request):
    subcategory_id = request.GET.get('subcategory_id')
    services = Service.objects.filter(subcategory_id=subcategory_id).values('id', 'name', 'price')
    return JsonResponse({'services': list(services)})