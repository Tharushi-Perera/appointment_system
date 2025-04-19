from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.home, name='home'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('book/confirm/', views.confirm_appointment, name='confirm_appointment'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
]
