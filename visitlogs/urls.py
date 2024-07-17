from django.urls import path
from .views import web_exit

urlpatterns = [
    path('exit/', web_exit,  name='trainer_page'),
]
