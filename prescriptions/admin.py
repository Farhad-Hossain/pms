from django.contrib import admin
from .models import Prescription, PrescriptionItem, Patient


class PrescriptionItemInline(admin.TabularInline):
    model = PrescriptionItem
    extra = 1


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'gender', 'phone', 'doctor']
    search_fields = ['name', 'phone']
    list_filter = ['gender', 'doctor']


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['pk', 'patient', 'doctor', 'date', 'diagnosis']
    search_fields = ['patient__name', 'doctor__name', 'diagnosis']
    list_filter = ['date', 'doctor']
    inlines = [PrescriptionItemInline]
