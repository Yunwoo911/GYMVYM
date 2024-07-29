from django.urls import path
from . import views

app_name = 'visitlogs'

urlpatterns = [
    path('web_exit/', views.web_exit, name='web_exit'),
    path('web_entrance/', views.web_entrance, name='web_entrance'),
    path('nfc_exit/', views.nfc_exit, name='nfc_exit'),
    path('nfc_entrance/', views.nfc_entrance, name='nfc_entrance'),
    path('nfc_enter_exit/', views.nfc_enter_exit, name='nfc_enter_exit'),
    # path('current_member/', views.current_member, name='current_member'),
    path('identify_nfc/', views.identify_nfc, name='identify_nfc'),
]