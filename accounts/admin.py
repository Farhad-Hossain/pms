from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(UserAdmin):
    list_display = ['email', 'name', 'specialization', 'phone', 'is_active']
    search_fields = ['email', 'name', 'specialization']
    ordering = ['email']
    fieldsets = UserAdmin.fieldsets + (
        ('Medical Info', {
            'fields': ('name', 'specialization', 'degrees', 'phone',
                       'clinic_name', 'clinic_address', 'bmdc_reg_no', 'signature')
        }),
    )
