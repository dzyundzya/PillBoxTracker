from django.contrib import admin

from .models import ActiveSubstance, Category, Pill, Manufacturer, MedicineForm


@admin.register(ActiveSubstance)
class ActiveSubstanceAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Pill)
class PillAdmin(admin.ModelAdmin):
    pass


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    pass


@admin.register(MedicineForm)
class MedicineFormAdmin(admin.ModelAdmin):
    pass
