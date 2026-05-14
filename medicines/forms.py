from django import forms
from .models import Medicine, MedicineCategory


class MedicineCategoryForm(forms.ModelForm):
    class Meta:
        model = MedicineCategory
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = [
            'name', 'generic_name', 'category', 'dosage_form',
            'strength', 'manufacturer', 'default_dosage',
            'default_duration', 'default_instructions', 'description'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        doctor = kwargs.pop('doctor', None)
        super().__init__(*args, **kwargs)
        if doctor:
            self.fields['category'].queryset = MedicineCategory.objects.filter(doctor=doctor)
        self.fields['category'].required = False
        self.fields['category'].empty_label = '-- No Category --'
