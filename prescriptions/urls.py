from django.urls import path
from . import views

app_name = 'prescriptions'

urlpatterns = [
    path('', views.prescription_list, name='prescription_list'),
    path('new/', views.prescription_create, name='prescription_create'),
    path('<int:pk>/', views.prescription_detail, name='prescription_detail'),
    path('<int:pk>/edit/', views.prescription_update, name='prescription_update'),
    path('<int:pk>/delete/', views.prescription_delete, name='prescription_delete'),
    path('<int:pk>/print/', views.prescription_print, name='prescription_print'),
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/add/', views.patient_create, name='patient_create'),
    path('patients/<int:pk>/edit/', views.patient_update, name='patient_update'),
]
