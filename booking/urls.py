from django.urls import path
from . import views
from .views import get_subcategories, get_services

app_name = 'booking'

# urls.py
urlpatterns = [
    path('', views.home, name='home'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('book/confirm/', views.confirm_appointment, name='confirm_appointment'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),
    path('get_services/', views.get_services, name='get_services'),
    path('book/choose-time/', views.choose_time, name='choose_time'),
    path('confirm-appointment/', views.confirm_appointment, name='confirm_appointment'),
    path('save-appointment/', views.save_appointment, name='save_appointment'),
    path('appointment-success/', views.appointment_success, name='appointment_success'),
    path('appointment/<int:appointment_id>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    path('appointment/<int:appointment_id>/reschedule/', views.reschedule_appointment, name='reschedule_appointment'),
]
