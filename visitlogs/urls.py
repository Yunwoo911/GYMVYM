from django.urls import path
from .views import web_exit
import views

urlpatterns = [
    path('web_exit/', web_exit, name='web_exit'),
    path('check-in/<str:nfc_uid>/', views.check_in, name='check_in'),
    path('check-out/<str:nfc_uid>/', views.check_out, name='check_out'),
]