from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Prescription, Patient, PrescriptionItem
from .forms import PrescriptionForm, PrescriptionItemForm, PrescriptionItemFormSet, PatientForm
from medicines.models import Medicine


# ── Patient Views ─────────────────────────────────────────────────────────────

@login_required
def patient_list(request):
    patients = Patient.objects.filter(doctor=request.user)
    q = request.GET.get('q', '').strip()
    if q:
        patients = patients.filter(name__icontains=q)
    return render(request, 'prescriptions/patient_list.html', {'patients': patients, 'q': q})


@login_required
def patient_create(request):
    form = PatientForm()
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.doctor = request.user
            patient.save()
            messages.success(request, f'Patient "{patient.name}" added.')
            return redirect('prescriptions:patient_list')
    return render(request, 'prescriptions/patient_form.html', {'form': form, 'title': 'Add Patient'})


@login_required
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk, doctor=request.user)
    form = PatientForm(instance=patient)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, f'Patient "{patient.name}" updated.')
            return redirect('prescriptions:patient_list')
    return render(request, 'prescriptions/patient_form.html', {'form': form, 'title': 'Edit Patient', 'patient': patient})


# ── Prescription Views ────────────────────────────────────────────────────────

@login_required
def prescription_list(request):
    prescriptions = Prescription.objects.filter(doctor=request.user).select_related('patient')
    q = request.GET.get('q', '').strip()
    if q:
        prescriptions = prescriptions.filter(patient__name__icontains=q)
    return render(request, 'prescriptions/prescription_list.html', {
        'prescriptions': prescriptions, 'q': q
    })


def _make_formset(request=None, instance=None, doctor=None, data=None):
    """Helper: build a PrescriptionItemFormSet with per-form doctor kwarg."""
    class DoctorItemFormSet(PrescriptionItemFormSet):
        def get_form_kwargs(self, index):
            kwargs = super().get_form_kwargs(index)
            kwargs['doctor'] = doctor
            return kwargs

    kwargs = {'instance': instance}
    if data:
        kwargs['data'] = data
    return DoctorItemFormSet(**kwargs)


@login_required
def prescription_create(request):
    today = timezone.localdate()
    p_form = PrescriptionForm(initial={'date': today})
    patient_form = PatientForm()
    formset = _make_formset(instance=Prescription(), doctor=request.user)
    patients = Patient.objects.filter(doctor=request.user)
    medicines_json = _medicines_json(request.user)

    if request.method == 'POST':
        p_form = PrescriptionForm(request.POST)
        formset = _make_formset(instance=Prescription(), doctor=request.user, data=request.POST)

        patient_id = request.POST.get('patient_id')
        if patient_id:
            patient = get_object_or_404(Patient, pk=patient_id, doctor=request.user)
        else:
            patient_form = PatientForm(request.POST)
            if patient_form.is_valid():
                patient = patient_form.save(commit=False)
                patient.doctor = request.user
                patient.save()
            else:
                return render(request, 'prescriptions/prescription_form.html', {
                    'p_form': p_form, 'patient_form': patient_form,
                    'formset': formset, 'patients': patients,
                    'medicines_json': medicines_json, 'title': 'New Prescription'
                })

        if p_form.is_valid() and formset.is_valid():
            prescription = p_form.save(commit=False)
            prescription.doctor = request.user
            prescription.patient = patient
            prescription.save()
            items = formset.save(commit=False)
            for item in items:
                item.prescription = prescription
                item.save()
            for obj in formset.deleted_objects:
                obj.delete()
            messages.success(request, 'Prescription created successfully.')
            return redirect('prescriptions:prescription_detail', pk=prescription.pk)

    return render(request, 'prescriptions/prescription_form.html', {
        'p_form': p_form,
        'patient_form': patient_form,
        'formset': formset,
        'patients': patients,
        'medicines_json': medicines_json,
        'title': 'New Prescription',
    })


@login_required
def prescription_update(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk, doctor=request.user)
    p_form = PrescriptionForm(instance=prescription)
    formset = _make_formset(instance=prescription, doctor=request.user)
    patients = Patient.objects.filter(doctor=request.user)
    medicines_json = _medicines_json(request.user)

    if request.method == 'POST':
        p_form = PrescriptionForm(request.POST, instance=prescription)
        formset = _make_formset(instance=prescription, doctor=request.user, data=request.POST)
        if p_form.is_valid() and formset.is_valid():
            p_form.save()
            items = formset.save(commit=False)
            for item in items:
                item.prescription = prescription
                item.save()
            for obj in formset.deleted_objects:
                obj.delete()
            messages.success(request, 'Prescription updated successfully.')
            return redirect('prescriptions:prescription_detail', pk=prescription.pk)

    return render(request, 'prescriptions/prescription_form.html', {
        'p_form': p_form,
        'patient_form': None,
        'formset': formset,
        'patients': patients,
        'medicines_json': medicines_json,
        'prescription': prescription,
        'title': 'Edit Prescription',
    })


@login_required
def prescription_detail(request, pk):
    prescription = get_object_or_404(
        Prescription.objects.select_related('patient', 'doctor').prefetch_related('items__medicine'),
        pk=pk, doctor=request.user
    )
    return render(request, 'prescriptions/prescription_detail.html', {'prescription': prescription})


@login_required
def prescription_delete(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk, doctor=request.user)
    if request.method == 'POST':
        prescription.delete()
        messages.success(request, 'Prescription deleted.')
        return redirect('prescriptions:prescription_list')
    return render(request, 'prescriptions/confirm_delete.html', {
        'object': prescription, 'cancel_url': 'prescriptions:prescription_list',
        'object_type': 'Prescription'
    })


@login_required
def prescription_print(request, pk):
    prescription = get_object_or_404(
        Prescription.objects.select_related('patient', 'doctor').prefetch_related('items__medicine'),
        pk=pk, doctor=request.user
    )
    return render(request, 'prescriptions/prescription_print.html', {'prescription': prescription})


def _medicines_json(doctor):
    import json
    medicines = list(Medicine.objects.filter(doctor=doctor).values(
        'id', 'name', 'strength', 'dosage_form',
        'default_dosage', 'default_duration', 'default_instructions'
    ))
    return json.dumps(medicines)
