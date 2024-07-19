from django.urls import path
from .views import web_exit

urlpatterns = [
    path('web_exit/', web_exit, name='web_exit'),
]