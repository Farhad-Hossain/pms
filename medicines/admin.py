from django.contrib import admin
from .models import Medicine, MedicineCategory


@admin.register(MedicineCategory)
class MedicineCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'doctor', 'description']
    search_fields = ['name', 'doctor__name']
    list_filter = ['doctor']


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'generic_name', 'dosage_form', 'strength', 'category', 'doctor']
    search_fields = ['name', 'generic_name', 'doctor__name']
    list_filter = ['dosage_form', 'category', 'doctor']
