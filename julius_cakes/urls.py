from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Custom Error Handlers
handler404 = 'bakery.views.custom_404'
handler500 = 'bakery.views.custom_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bakery.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
