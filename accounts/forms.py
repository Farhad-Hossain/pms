from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Doctor


class DoctorRegistrationForm(UserCreationForm):
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Full Name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email Address'})
    )
    specialization = forms.CharField(
        max_length=200, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. General Physician, Cardiologist'})
    )
    degrees = forms.CharField(
        max_length=300, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. MBBS, MD, FCPS'})
    )
    phone = forms.CharField(
        max_length=20, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number'})
    )
    clinic_name = forms.CharField(
        max_length=300, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Clinic / Hospital Name'})
    )
    clinic_address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Clinic Address', 'rows': 3})
    )
    bmdc_reg_no = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'BMDC Registration Number'})
    )

    class Meta:
        model = Doctor
        fields = [
            'name', 'email', 'specialization', 'degrees',
            'phone', 'clinic_name', 'clinic_address', 'bmdc_reg_no',
            'password1', 'password2',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.name = self.cleaned_data['name']
        if commit:
            user.save()
        return user


class DoctorLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Email Address', 'autofocus': True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            'name', 'specialization', 'degrees', 'phone',
            'clinic_name', 'clinic_address', 'bmdc_reg_no', 'signature'
        ]
        widgets = {
            'clinic_address': forms.Textarea(attrs={'rows': 3}),
        }
