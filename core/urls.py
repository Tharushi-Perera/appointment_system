from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from booking import views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('login')),  # Redirect root URL to login initially
    path('admin/', admin.site.urls),

    # Application URLs
    path('', include('booking.urls', namespace='booking')),
    path('services/', include('salon_services.urls')),
    path('stylists/', TemplateView.as_view(template_name='stylists.html'), name='stylists'),
    path('', views.home, name='home'),

    # Authentication URLs
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
