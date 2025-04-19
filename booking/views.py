import datetime
from django.shortcuts import render, redirect
from .forms import AppointmentForm
from .models import Appointment, Service
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
    return render(request, 'home.html', {'services': services})


#@login_required
def book_appointment(request):
    form = AppointmentForm()
    time_slots = []

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            service = form.cleaned_data['service']
            date = form.cleaned_data['date']
            duration = service.duration

            # Working hours (e.g., 9 AM to 5 PM)
            start_time = datetime.datetime.combine(date, datetime.time(9, 0))
            end_time = datetime.datetime.combine(date, datetime.time(17, 0))

            # Get already booked times
            existing = Appointment.objects.filter(date=date)
            booked_times = [datetime.datetime.combine(date, a.time) for a in existing]

            slots = generate_time_slots(start_time, end_time, duration)

            # Filter out already booked
            available_slots = []
            for slot in slots:
                slot_dt = datetime.datetime.combine(date, datetime.datetime.strptime(slot, "%H:%M").time())
                if slot_dt not in booked_times:
                    available_slots.append(slot)

            request.session['appointment_data'] = form.cleaned_data
            return render(request, 'booking/choose_time.html', {
                'slots': available_slots,
                'service': service,
                'date': date,
            })

    return render(request, 'booking/book.html', {'form': form})


#@login_required
def confirm_appointment(request):
    if request.method == 'POST':
        time_str = request.POST.get('time')
        time_obj = datetime.datetime.strptime(time_str, "%H:%M").time()

        data = request.session.get('appointment_data')
        service = Service.objects.get(id=data['service'].id)

        Appointment.objects.create(
            user=request.user,
            service=service,
            date=data['date'],
            time=time_obj,
            status='Pending'
        )
        return redirect('user_dashboard')  # or confirmation page

    return redirect('book')


#@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(user=request.user).order_by('-date')
    return render(request, 'booking/my_appointments.html', {'appointments': appointments})
