from django.contrib import admin
from .models import Service, Appointment

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'duration']
    search_fields = ['title']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'service', 'date', 'time', 'status']
    list_filter = ['status', 'date']
    search_fields = ['user__username', 'service__title']
