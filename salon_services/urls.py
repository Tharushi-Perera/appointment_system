from django.urls import path
from . import views

urlpatterns = [
    path('', views.services_main, name='services_main'),
    path('hair/', views.hair_services, name='hair_services'),
    path('skin/', views.skin_services, name='skin_services'),
    path('body/', views.body_services, name='body_services'),
    path('nails/', views.nail_services, name='nail_services'),
    path('bridal/', views.bridal_services, name='bridal_services'),
]
