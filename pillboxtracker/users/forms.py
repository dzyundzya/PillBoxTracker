from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class CustomUserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'username', 'birthday')
        widgets = {
            'birthday': forms.DateInput(attrs={
                'type': 'date',
                'placeholder': 'Выберите дату рождения'
            })
        }


class CustomUserUpdateForm(CustomUserCreateForm):
    class Meta(CustomUserCreateForm.Meta):
        fields = ('first_name', 'last_name', 'username', 'bio',)