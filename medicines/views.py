from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Medicine, MedicineCategory
from .forms import MedicineForm, MedicineCategoryForm


# ── Medicine Category Views ──────────────────────────────────────────────────

@login_required
def category_list(request):
    categories = MedicineCategory.objects.filter(doctor=request.user)
    return render(request, 'medicines/category_list.html', {'categories': categories})


@login_required
def category_create(request):
    form = MedicineCategoryForm()
    if request.method == 'POST':
        form = MedicineCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.doctor = request.user
            category.save()
            messages.success(request, f'Category "{category.name}" created.')
            return redirect('medicines:category_list')
    return render(request, 'medicines/category_form.html', {'form': form, 'title': 'Add Category'})


@login_required
def category_update(request, pk):
    category = get_object_or_404(MedicineCategory, pk=pk, doctor=request.user)
    form = MedicineCategoryForm(instance=category)
    if request.method == 'POST':
        form = MedicineCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'Category "{category.name}" updated.')
            return redirect('medicines:category_list')
    return render(request, 'medicines/category_form.html', {'form': form, 'title': 'Edit Category', 'category': category})


@login_required
def category_delete(request, pk):
    category = get_object_or_404(MedicineCategory, pk=pk, doctor=request.user)
    if request.method == 'POST':
        name = category.name
        category.delete()
        messages.success(request, f'Category "{name}" deleted.')
        return redirect('medicines:category_list')
    return render(request, 'medicines/confirm_delete.html', {
        'object': category, 'cancel_url': 'medicines:category_list', 'object_type': 'Category'
    })


# ── Medicine Views ────────────────────────────────────────────────────────────

@login_required
def medicine_list(request):
    medicines = Medicine.objects.filter(doctor=request.user).select_related('category')
    categories = MedicineCategory.objects.filter(doctor=request.user)
    selected_category = request.GET.get('category')
    search_q = request.GET.get('q', '').strip()
    if selected_category:
        medicines = medicines.filter(category_id=selected_category)
    if search_q:
        medicines = medicines.filter(name__icontains=search_q)
    return render(request, 'medicines/medicine_list.html', {
        'medicines': medicines,
        'categories': categories,
        'selected_category': selected_category,
        'search_q': search_q,
    })


@login_required
def medicine_create(request):
    form = MedicineForm(doctor=request.user)
    if request.method == 'POST':
        form = MedicineForm(request.POST, doctor=request.user)
        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.doctor = request.user
            medicine.save()
            messages.success(request, f'Medicine "{medicine.name}" added to your catalog.')
            return redirect('medicines:medicine_list')
    return render(request, 'medicines/medicine_form.html', {'form': form, 'title': 'Add Medicine'})


@login_required
def medicine_update(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk, doctor=request.user)
    form = MedicineForm(instance=medicine, doctor=request.user)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine, doctor=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Medicine "{medicine.name}" updated.')
            return redirect('medicines:medicine_list')
    return render(request, 'medicines/medicine_form.html', {
        'form': form, 'title': 'Edit Medicine', 'medicine': medicine
    })


@login_required
def medicine_delete(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk, doctor=request.user)
    if request.method == 'POST':
        name = medicine.name
        medicine.delete()
        messages.success(request, f'Medicine "{name}" removed from catalog.')
        return redirect('medicines:medicine_list')
    return render(request, 'medicines/confirm_delete.html', {
        'object': medicine, 'cancel_url': 'medicines:medicine_list', 'object_type': 'Medicine'
    })
