from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/registration/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('pillbox/', include('pillbox.urls')),
    path('', include('pages.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
