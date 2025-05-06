from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from booking import views as booking_views
from django.conf import settings
from django.conf.urls.static import static
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home Page
    path('', booking_views.home, name='home'),

    # Application URLs
    path('book/', include('booking.urls', namespace='booking')),
    path('services/', include('salon_services.urls')),
    path('stylists/', TemplateView.as_view(template_name='stylists.html'), name='stylists'),
    path('contact/', booking_views.contact, name='contact'),
    path('offers/', booking_views.offers, name='offers'),
    path('profile/', views.profile_view, name='profile'),

    # Authentication
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
