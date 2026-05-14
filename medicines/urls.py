from django.urls import path
from . import views

app_name = 'medicines'

urlpatterns = [
    path('', views.medicine_list, name='medicine_list'),
    path('add/', views.medicine_create, name='medicine_create'),
    path('<int:pk>/edit/', views.medicine_update, name='medicine_update'),
    path('<int:pk>/delete/', views.medicine_delete, name='medicine_delete'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
]
