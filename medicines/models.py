from django.db import models
from accounts.models import Doctor


class MedicineCategory(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='medicine_categories')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Medicine Categories'
        unique_together = ('doctor', 'name')
        ordering = ['name']

    def __str__(self):
        return self.name


class Medicine(models.Model):
    DOSAGE_FORM_CHOICES = [
        ('tablet', 'Tablet'),
        ('capsule', 'Capsule'),
        ('syrup', 'Syrup'),
        ('injection', 'Injection'),
        ('cream', 'Cream / Ointment'),
        ('drops', 'Drops'),
        ('inhaler', 'Inhaler'),
        ('suppository', 'Suppository'),
        ('powder', 'Powder'),
        ('patch', 'Patch'),
        ('other', 'Other'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='medicines')
    category = models.ForeignKey(
        MedicineCategory, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='medicines'
    )
    name = models.CharField(max_length=300)
    generic_name = models.CharField(max_length=300, blank=True)
    manufacturer = models.CharField(max_length=300, blank=True)
    dosage_form = models.CharField(max_length=50, choices=DOSAGE_FORM_CHOICES, default='tablet')
    strength = models.CharField(max_length=100, blank=True, help_text='e.g. 500mg, 10mg/5ml')
    default_dosage = models.CharField(
        max_length=200, blank=True,
        help_text='e.g. 1+0+1 (morning, noon, night)'
    )
    default_duration = models.CharField(max_length=100, blank=True, help_text='e.g. 7 days, 2 weeks')
    default_instructions = models.CharField(max_length=300, blank=True, help_text='e.g. After meal')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        strength = f" {self.strength}" if self.strength else ""
        return f"{self.name}{strength} ({self.get_dosage_form_display()})"
