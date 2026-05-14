from django.db import models
from accounts.models import Doctor
from medicines.models import Medicine


class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('', 'Unknown'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='patients')
    name = models.CharField(max_length=200)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, help_text='kg')
    allergies = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Prescription(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='prescriptions')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    date = models.DateField()
    serial_no = models.CharField(max_length=50, blank=True)
    chief_complaint = models.TextField(blank=True, verbose_name='Chief Complaint / History')
    diagnosis = models.TextField(blank=True)
    investigations = models.TextField(blank=True, help_text='Blood test, X-ray, etc.')
    advice = models.TextField(blank=True, verbose_name='Advice / Notes')
    follow_up_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"Rx #{self.pk} – {self.patient.name} ({self.date})"


class PrescriptionItem(models.Model):
    FREQUENCY_CHOICES = [
        ('1+0+0', '1+0+0 (Morning only)'),
        ('0+1+0', '0+1+0 (Noon only)'),
        ('0+0+1', '0+0+1 (Night only)'),
        ('1+0+1', '1+0+1 (Morning & Night)'),
        ('1+1+0', '1+1+0 (Morning & Noon)'),
        ('1+1+1', '1+1+1 (Three times daily)'),
        ('1+1+1+1', '1+1+1+1 (Four times daily)'),
        ('sos', 'SOS (As needed)'),
        ('custom', 'Custom'),
    ]

    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(
        Medicine, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='prescription_items'
    )
    custom_medicine = models.CharField(max_length=300, blank=True, help_text='If not in catalog')
    dosage = models.CharField(max_length=200, blank=True)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, blank=True)
    duration = models.CharField(max_length=100, blank=True, help_text='e.g. 7 days, 2 weeks')
    instructions = models.CharField(max_length=300, blank=True, help_text='e.g. After meal')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def medicine_name(self):
        if self.medicine:
            return str(self.medicine)
        return self.custom_medicine

    def __str__(self):
        return self.medicine_name()
