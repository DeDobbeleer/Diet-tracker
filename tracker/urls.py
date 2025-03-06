# tracker/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.entry_list, name='entry_list'),
    path('add/', views.add_entry, name='add_entry'),
    path('edit/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('delete/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    path('export/', views.export_csv, name='export_csv'),
    path('import/', views.import_csv, name='import_csv'),
]