from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username',)
    search_fields = ('email', 'username',)
    fields = (
        ('email', 'username', 'avatar'),
        ('first_name', 'last_name', 'telegram_chat_id'),
        ('birthday', 'gender',),
        ('bio',),
        ('password',)
    )


admin.site.empty_value_display = 'Не задано'
