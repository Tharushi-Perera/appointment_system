from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_appointment, name='book'),
    path('confirm/', views.confirm_appointment, name='confirm_appointment'),
]
