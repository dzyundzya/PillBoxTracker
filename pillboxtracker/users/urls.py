from django.urls import include, path

from users import views

app_name = 'users'

urlpatterns = [
    path(
        'registration/', views.UserRegistration.as_view(), name='registration'
    ),
    path('', include('django.contrib.auth.urls')),
]
