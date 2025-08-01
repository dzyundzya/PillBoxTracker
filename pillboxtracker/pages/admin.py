from django.contrib import admin

from .models import Accordion


@admin.register(Accordion)
class AccordionAdmin(admin.ModelAdmin):
    pass
