from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import AppointmentForm
from .models import Appointment
from .models import ServiceSubCategory, Service
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from datetime import datetime, date, time, timedelta
from django.utils import timezone
from .models import ServiceCategory
from decimal import Decimal

# Constants for business hours
OPENING_TIME = time(9, 0)  # 9 AM
CLOSING_TIME = time(21, 0) # 9 PM


def generate_time_slots(date, duration_minutes):
    slots = []
    start_datetime = datetime.combine(date, time(9, 0))  # 9 AM
    end_datetime = datetime.combine(date, time(21, 0))  # 9 PM

    current = start_datetime
    while current + timedelta(minutes=duration_minutes) <= end_datetime:
        slots.append({
            'value': current.time().strftime('%H:%M:%S'),  # Storage format
            'display': current.time().strftime('%I:%M %p')  # Display format
        })
        current += timedelta(minutes=duration_minutes)
    return slots


def home(request):
    services = Service.objects.all()
    return render(request, 'home.html', {'listing_services': services})


@login_required
def book_appointment(request):
    categories = ServiceCategory.objects.prefetch_related(
        'subcategories__services'
    ).order_by('display_order')

    if request.method == 'POST':
        # Get selected service IDs from the form
        selected_service_ids = request.POST.getlist('services')

        if not selected_service_ids:
            # Handle case where no services are selected
            return render(request, 'booking/book.html', {
                'categories': categories,
                'error': 'Please select at least one service'
            })

        # Store in session (we'll just use the first service for time selection)
        first_service = Service.objects.get(id=selected_service_ids[0])
        request.session['appointment_data'] = {
            'service_ids': selected_service_ids,
            'date': request.POST.get('date')
        }
        return redirect('booking:choose_time')

    return render(request, 'booking/book.html', {
        'categories': categories,
        'form': AppointmentForm()  # For the date picker
    })


@login_required
def confirm_appointment(request):
    appointment_data = request.session.get('appointment_data')
    if not appointment_data or 'time' not in request.GET:
        return redirect('booking:book_appointment')

    try:
        services = Service.objects.filter(id__in=appointment_data['service_ids'])
        total_duration = sum(service.duration_minutes for service in services)

        # Handle date
        date_str = appointment_data['date']
        appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date() if isinstance(date_str, str) else date_str

        # Handle time - accepts both "HH:MM:SS" and "HH:MM AM/PM"
        time_str = request.GET['time']
        try:
            # Try parsing as 24-hour format first
            appointment_time = datetime.strptime(time_str, '%H:%M:%S').time()
        except ValueError:
            # If that fails, try 12-hour format
            appointment_time = datetime.strptime(time_str, '%I:%M %p').time()

        return render(request, 'booking/confirm_appointment.html', {
            'services': services,
            'date': appointment_date,
            'time': appointment_time.strftime('%I:%M %p'),  # Display as 12-hour format
            'total_duration': total_duration
        })
    except Exception as e:
        print(f"Error in confirmation: {e}")
        return redirect('booking:book_appointment')


@login_required
def save_appointment(request):
    if request.method == 'POST':
        appointment_data = request.session.get('appointment_data')
        if not appointment_data:
            return redirect('booking:book_appointment')

        try:
            services = Service.objects.filter(id__in=appointment_data['service_ids'])
            time_str = request.POST.get('time')
            date_str = appointment_data['date']

            # Parse date
            appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date() if isinstance(date_str, str) else date_str

            # Parse time - handles both formats
            try:
                appointment_time = datetime.strptime(time_str, '%H:%M:%S').time()
            except ValueError:
                appointment_time = datetime.strptime(time_str, '%I:%M %p').time()

            # Save to session
            request.session['last_appointment'] = {
                'services': [s.name for s in services],
                'date': appointment_date.strftime("%B %d, %Y"),
                'time': appointment_time.strftime('%I:%M %p'),
                'total': float(sum(service.price for service in services))
            }

            # Create appointments
            for service in services:
                Appointment.objects.create(
                    user=request.user,
                    service=service,
                    date=appointment_date,
                    time=appointment_time,
                    status='Pending'
                )

            del request.session['appointment_data']
            request.session.modified = True

            return redirect('booking:appointment_success')
        except Exception as e:
            print(f"Error saving appointment: {e}")
            return redirect('booking:book_appointment')
    return redirect('booking:book_appointment')


@login_required
def appointment_success(request):
    appointment_data = request.session.get('last_appointment')  # Keep this key

    if not appointment_data:
        return redirect('booking:book_appointment')

    # Pass the correct data to template
    return render(request, 'booking/appointment_success.html', {
        'appointment': {
            'date': appointment_data['date'],
            'time': appointment_data['time'],
            'services': appointment_data['services'],
            'total': appointment_data['total']
        }
    })

@login_required
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


@login_required
def choose_time(request):
    appointment_data = request.session.get('appointment_data')
    if not appointment_data:
        return redirect('booking:book_appointment')

    try:
        # Get selected services and date
        primary_service = Service.objects.get(id=appointment_data['service_ids'][0])
        date = datetime.strptime(appointment_data['date'], '%Y-%m-%d').date()
        selected_services = Service.objects.filter(id__in=appointment_data['service_ids'])
        total_duration = sum(s.duration_minutes for s in selected_services)

        # Generate ALL possible slots
        all_slots = generate_time_slots(date, primary_service.duration_minutes)

        # Fetch existing appointments for the date
        existing_appointments = Appointment.objects.filter(
            date=date,
            status__in=['Pending', 'Confirmed']  # Ignore cancelled/completed
        ).values_list('time', flat=True)

        # Convert booked times to match slot format ("HH:MM:SS")
        booked_times = [t.strftime('%H:%M:%S') for t in existing_appointments]

        # Filter out occupied slots
        available_slots = [
            slot for slot in all_slots
            if slot['value'] not in booked_times
        ]

        return render(request, 'booking/choose_time.html', {
            'services': selected_services,
            'primary_service': primary_service,
            'date': date,
            'slots': available_slots,  # Only show available slots
            'total_duration': total_duration
        })

    except (Service.DoesNotExist, KeyError, ValueError) as e:
        messages.error(request, "Invalid appointment data")
        return redirect('booking:book_appointment')

@login_required
@require_POST
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
    appointment.status = 'Cancelled'
    appointment.save()
    messages.success(request, f"Appointment for {appointment.service.name} has been cancelled.")
    return redirect('booking:my_appointments')


@login_required
def reschedule_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)

    if request.method == 'POST':
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')

        try:
            # Validate and update appointment
            appointment.date = datetime.strptime(date_str, '%Y-%m-%d').date()
            appointment.time = datetime.strptime(time_str, '%H:%M:%S').time()
            appointment.status = 'Rescheduled'
            appointment.save()

            messages.success(request, "Appointment rescheduled successfully!")
            return redirect('booking:my_appointments')
        except Exception as e:
            messages.error(request, f"Error rescheduling: {str(e)}")

    # Generate time slots for the current appointment date by default
    time_slots = generate_time_slots(appointment.date, appointment.service.duration_minutes)

    return render(request, 'booking/reschedule.html', {
        'appointment': appointment,
        'time_slots': time_slots,
        'min_date': timezone.now().date(),
        'max_date': timezone.now().date() + timedelta(days=60)  # 2 months in future
    })


