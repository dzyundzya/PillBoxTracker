from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .forms import CustomUserCreateForm


class UserRegistration(CreateView):
    form_class = CustomUserCreateForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('pages:homepage')
