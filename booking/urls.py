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
]
