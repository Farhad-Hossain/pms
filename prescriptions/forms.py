from django import forms
from django.forms import inlineformset_factory
from .models import Prescription, PrescriptionItem, Patient
from medicines.models import Medicine


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'gender', 'phone', 'address', 'blood_group', 'weight', 'allergies']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
            'allergies': forms.Textarea(attrs={'rows': 2}),
        }


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = [
            'date', 'serial_no', 'chief_complaint', 'diagnosis',
            'investigations', 'advice', 'follow_up_date'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'follow_up_date': forms.DateInput(attrs={'type': 'date'}),
            'chief_complaint': forms.Textarea(attrs={'rows': 3}),
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
            'investigations': forms.Textarea(attrs={'rows': 2}),
            'advice': forms.Textarea(attrs={'rows': 3}),
        }


class PrescriptionItemForm(forms.ModelForm):
    class Meta:
        model = PrescriptionItem
        fields = ['medicine', 'custom_medicine', 'dosage', 'frequency', 'duration', 'instructions']
        widgets = {
            'instructions': forms.TextInput(attrs={'placeholder': 'e.g. After meal'}),
            'dosage': forms.TextInput(attrs={'placeholder': 'e.g. 1 tablet'}),
            'duration': forms.TextInput(attrs={'placeholder': 'e.g. 7 days'}),
            'custom_medicine': forms.TextInput(attrs={'placeholder': 'Type medicine name if not in catalog'}),
        }

    def __init__(self, *args, **kwargs):
        doctor = kwargs.pop('doctor', None)
        super().__init__(*args, **kwargs)
        if doctor:
            self.fields['medicine'].queryset = Medicine.objects.filter(doctor=doctor)
        self.fields['medicine'].required = False
        self.fields['medicine'].empty_label = '-- Select from catalog --'


PrescriptionItemFormSet = inlineformset_factory(
    Prescription,
    PrescriptionItem,
    form=PrescriptionItemForm,
    extra=3,
    can_delete=True,
    min_num=0,
)
