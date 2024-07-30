from django.urls import path, include
from . import views

app_name = 'equipment'

urlpatterns = [
    path('show/', views.show_equipments, name='show_equipments'),
    path('reserve/<int:equipment_id>/', views.reserve_equipment, name='reserve_equipment'),
    path('status/', views.equipment_status, name='equipment_status'),
    path('tag_equipment/', views.tag_equipment, name='tag_equipment'),
    path('show_reserve/', views.show_reserve, name='show_reserve'),
]