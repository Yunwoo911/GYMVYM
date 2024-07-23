from django.urls import path
from . import views


urlpatterns = [
    path('web_exit/', views.web_exit, name='web_exit'),
    path('web_entrance/', views.web_entrance, name='web_entrance'),
]