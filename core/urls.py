from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from booking import views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('login')),   # Redirect root to login initially
    path('admin/', admin.site.urls),
    path('', include('booking.urls', namespace='booking')),  # Booking app
    path('services/', include('salon_services.urls')),       # Salon services
    path('stylists/', TemplateView.as_view(template_name='stylists.html'), name='stylists'),  # Static stylist page
    path('', views.home, name='home'),                        # Home page (keep this LAST for "/" to go here)
    path('accounts/', include('accounts.urls')),              # Your views (register, login, logout)
    path('accounts/', include('allauth.urls')),               # Django-allauth (Google login, etc.)
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
