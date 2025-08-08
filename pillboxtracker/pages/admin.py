from django.contrib import admin

from .models import Accordion


@admin.register(Accordion)
class AccordionAdmin(admin.ModelAdmin):
    list_display = ('title', 'strong_text', 'group')
    list_editable = ('group',)
    search_fields = ('title',)
    list_filter = ('group',)


admin.site.empty_value_display = 'Не задано'
