from django.contrib import admin
from django.urls import path, include
from booking import views  # ✅ Make sure to import views from booking
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('booking.urls', namespace='booking')),
    path('', include('accounts.urls')),
    path('', views.home, name='home'),  # ✅ This should be from booking.views
]

# ✅ This enables serving static files like CSS and images in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
