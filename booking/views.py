import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import AppointmentForm
from .models import Appointment, Service
from .models import Service
from .models import ServiceSubCategory, Service
from django.shortcuts import get_object_or_404
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
from .models import ServiceCategory


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


#@login_required
# booking/views.py
def confirm_appointment(request):
    if request.method == 'POST':
        appointment_data = request.session.get('appointment_data')
        if appointment_data:
            try:
                services = Service.objects.filter(id__in=appointment_data['service_ids'])
                selected_time = request.POST.get('time')

                # Create appointment for each service
                for service in services:
                    Appointment.objects.create(
                        user=request.user,
                        service=service,
                        date=appointment_data['date'],
                        time=selected_time,
                        status='Pending'
                    )

                # Clear session data
                if 'appointment_data' in request.session:
                    del request.session['appointment_data']

                return redirect('booking:my_appointments')

            except (KeyError, Service.DoesNotExist):
                pass

    return redirect('booking:book_appointment')


from django.shortcuts import get_object_or_404


def choose_time(request):
    appointment_data = request.session.get('appointment_data')
    if not appointment_data:
        return redirect('booking:book_appointment')

    try:
        services = Service.objects.filter(id__in=appointment_data['service_ids'])
        total_duration = sum(service.duration_minutes for service in services)
        date = datetime.date.fromisoformat(appointment_data['date'])

        # Generate time slots (9 AM to 5 PM)
        start_time = datetime.datetime.combine(date, datetime.time(9, 0))
        end_time = datetime.datetime.combine(date, datetime.time(17, 0))
        slots = generate_time_slots(start_time, end_time, services[0].duration_minutes)

        return render(request, 'booking/choose_time.html', {
            'services': services,
            'date': date,
            'slots': slots,
            'total_duration': total_duration
        })
    except (Service.DoesNotExist, KeyError, ValueError):
        return redirect('booking:book_appointment')


def confirm_appointment(request):
    appointment_data = request.session.get('appointment_data')
    if not appointment_data or 'time' not in request.GET:
        return redirect('booking:book_appointment')

    try:
        services = Service.objects.filter(id__in=appointment_data['service_ids'])
        total_duration = sum(service.duration_minutes for service in services)
        date = datetime.date.fromisoformat(appointment_data['date'])

        return render(request, 'booking/confirm_appointment.html', {
            'services': services,
            'date': date,
            'time': request.GET['time'],
            'total_duration': total_duration
        })
    except (Service.DoesNotExist, KeyError, ValueError):
        return redirect('booking:book_appointment')


from decimal import Decimal
def save_appointment(request):
    if request.method == 'POST':
        appointment_data = request.session.get('appointment_data')
        if not appointment_data:
            return redirect('booking:book_appointment')

        try:
            services = Service.objects.filter(id__in=appointment_data['service_ids'])
            time = request.POST.get('time')
            date = datetime.date.fromisoformat(appointment_data['date'])

            # Convert Decimal to float for session storage
            total = float(sum(service.price for service in services))

            # Store appointment details in session before redirect
            request.session['last_appointment_details'] = {
                'services': [s.name for s in services],
                'date': date.strftime("%B %d, %Y"),
                'time': time,
                'total': total  # Now storing as float instead of Decimal
            }

            # Create appointment for each service
            for service in services:
                Appointment.objects.create(
                    user=request.user,
                    service=service,
                    date=date,
                    time=time,
                    status='Pending'
                )

            # Clear temporary session data but keep last appointment
            del request.session['appointment_data']

            # Save the session explicitly
            request.session.modified = True

            return redirect('booking:appointment_success')
        except Exception as e:
            print(f"Error saving appointment: {e}")
            return redirect('booking:book_appointment')

    return redirect('booking:book_appointment')

def appointment_success(request):
    appointment_data = request.session.get('last_appointment')

    if not appointment_data:
        return redirect('booking:book_appointment')

    # Clear the session data after displaying
    if 'last_appointment' in request.session:
        del request.session['last_appointment']

    return render(request, 'booking/appointment_success.html', {
        'appointment': appointment_data
    })


#@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(user=request.user).order_by('-date')
    return render(request, 'booking/my_appointments.html', {'appointments': appointments})

def offers(request):
    return render(request, 'offers.html')
  
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
    appointment_data = request.session.get('appointment_data')
    if not appointment_data:
        return redirect('booking:book_appointment')

    try:
        # Get the primary service (first selected)
        primary_service = Service.objects.get(id=appointment_data['service_ids'][0])
        date = datetime.date.fromisoformat(appointment_data['date'])

        # Generate time slots based on the primary service duration
        start_time = datetime.datetime.combine(date, datetime.time(9, 0))  # 9 AM
        end_time = datetime.datetime.combine(date, datetime.time(17, 0))   # 5 PM
        slots = generate_time_slots(start_time, end_time, primary_service.duration_minutes)

        # Get all selected services for display
        selected_services = Service.objects.filter(id__in=appointment_data['service_ids'])

        return render(request, 'booking/choose_time.html', {
            'services': selected_services,
            'primary_service': primary_service,
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

def contact(request):
    return render(request, 'contact.html')
