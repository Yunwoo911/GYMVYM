# gyms/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')  # 'home.html' 템플릿을 렌더링
