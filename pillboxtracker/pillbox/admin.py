from django.contrib import admin

from .models import (
    ActiveSubstance, Category, Manufacturer,
    MedicineForm, Pill, Pillbox, ReminderTime
)


@admin.register(ActiveSubstance)
class ActiveSubstanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_editable = ('slug',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Pill)
class PillAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published', 'author',)
    search_fields = ('name', 'manufacturer',)
    list_filter = ('medicine_form',)
    list_editable = ('is_published',)
    fields = (
        ('name', 'author', 'is_published'),
        ('manufacturer', 'medicine_form', 'category'),
        ('active_substance',),
        ('description',),
        ('pub_date', 'image')
    )


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name',)
    list_filter = ('country',)
    list_editable = ('country',)


@admin.register(MedicineForm)
class MedicineFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_editable = ('slug',)


@admin.register(Pillbox)
class PillboxAdmin(admin.ModelAdmin):
    list_display = (
        'pill', 'user', 'is_active',
        'amount', 'daily_count', 'display_reminder_time'
    )
    search_fields = ('user', 'pill')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    fields = (
        ('pill', 'user', 'is_active'),
        ('amount', 'daily_count', 'start_date'),
        ('reminder_time',),
    )


@admin.register(ReminderTime)
class ReminderTimeAdmin(admin.ModelAdmin):
    list_display = ('time',)
    search_fields = ('time',)


admin.site.empty_value_display = 'Не задано'
