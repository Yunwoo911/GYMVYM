# gyms/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 기본 경로로 접근했을 때 'home' 뷰를 호출
]
