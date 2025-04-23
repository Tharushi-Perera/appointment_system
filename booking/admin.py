from django.contrib import admin
from .models import ServiceCategory, ServiceSubCategory, Service, Appointment

admin.site.register(ServiceCategory)
admin.site.register(ServiceSubCategory)
admin.site.register(Service)
admin.site.register(Appointment)
