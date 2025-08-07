from django.urls import path

from users import views


app_name = 'users'

urlpatterns = [
    path(
        '', views.UserRegistration.as_view(), name='registration'
    ),
]
