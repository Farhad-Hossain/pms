from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DoctorRegistrationForm, DoctorLoginForm, DoctorProfileForm
from medicines.models import Medicine
from prescriptions.models import Prescription


def register_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    form = DoctorRegistrationForm()
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, Dr. {user.name}! Your account has been created.')
            return redirect('accounts:dashboard')
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    form = DoctorLoginForm()
    if request.method == 'POST':
        form = DoctorLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, Dr. {user.name}!')
            next_url = request.GET.get('next', 'accounts:dashboard')
            return redirect(next_url)
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')


@login_required
def dashboard_view(request):
    doctor = request.user
    medicine_count = Medicine.objects.filter(doctor=doctor).count()
    prescription_count = Prescription.objects.filter(doctor=doctor).count()
    recent_prescriptions = Prescription.objects.filter(doctor=doctor).order_by('-created_at')[:5]
    context = {
        'doctor': doctor,
        'medicine_count': medicine_count,
        'prescription_count': prescription_count,
        'recent_prescriptions': recent_prescriptions,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile_view(request):
    doctor = request.user
    form = DoctorProfileForm(instance=doctor)
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    return render(request, 'accounts/profile.html', {'form': form, 'doctor': doctor})
