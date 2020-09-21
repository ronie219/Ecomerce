from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.urls import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('course/', include('course.urls'), name='course'),
    path('membership/', include('Membership.urls'), name='membership'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
