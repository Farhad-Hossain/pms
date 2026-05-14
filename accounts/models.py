from django.contrib.auth.models import AbstractUser
from django.db import models


class Doctor(AbstractUser):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    specialization = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    clinic_name = models.CharField(max_length=300, blank=True)
    clinic_address = models.TextField(blank=True)
    signature = models.ImageField(upload_to='signatures/', blank=True, null=True)
    bmdc_reg_no = models.CharField(max_length=100, blank=True, verbose_name='BMDC Reg. No.')
    degrees = models.CharField(max_length=300, blank=True, help_text='e.g. MBBS, MD, FCPS')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']

    def __str__(self):
        return f"Dr. {self.name}"

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'
