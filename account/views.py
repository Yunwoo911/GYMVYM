from .models import CustomUser
from rest_framework import generics
from .serializers import RegisterSerializer, LoginSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def get(self, request):
        return render(request, 'signup.html')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            # 로그인 화면으로 리다이렉트
            return redirect(reverse('login'))
        except Exception as e:
            return render(request, 'signup.html', {'errors': serializer.errors})

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data  # validate()의 리턴값인 token을 받아온다.
            user = token.user
            login(request, user)
            return redirect('home')  # URL name for the home view
        return render(request, 'login.html', {'errors': serializer.errors})

@login_required
def home_view(request):
    return render(request, 'home.html')

@login_required
def profile_view(request):
    return render(request, 'profile.html')

def check_email_duplicate(request):
    email = request.GET.get('email', None)
    if CustomUser.objects.filter(email=email).exists():
        return JsonResponse({'is_duplicate': True})
    else:
        return JsonResponse({'is_duplicate': False})


