from django import forms

from .models import Comment, Pill, Pillbox


class PillForm(forms.ModelForm):
    class Meta:
        model = Pill
        fields = (
            'name', 'image', 'description', 'pub_date',
            'manufacturer', 'medicine_form', 'active_substance',
            'category', 'is_published',
        )
        widgets = {
            'pub_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'placeholder': 'Выберите дату и время публикации'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'rows': 10, 'cols': 10,
                    'placeholder': 'Введите описание препарата'
                }
            ),
            'name': forms.TextInput(
                attrs={'placeholder': 'Введите название препарата'}
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class PillBoxForm(forms.ModelForm):

    class Meta:
        model = Pillbox
        fields = ('pill', 'amount', 'daily_count', 'reminder_time')