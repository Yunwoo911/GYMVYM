from .models import CustomUser, EmailVerification
from rest_framework import generics
from .serializers import RegisterSerializer, LoginSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import timedelta
from django.utils import timezone
from .forms import NFCForm
import uuid
import random
import string
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import json

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

@login_required
def update_nfc_view(request):
    if request.method == 'POST':
        form = NFCForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # 프로필 URL 네임
    else:
        form = NFCForm(instance=request.user)
    
    return render(request, 'update_nfc.html', {'form': form})

def send_verification_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        user = CustomUser.objects.filter(email=email).first()
        
        if user:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            EmailVerification.objects.create(
                user=user,
                verification_code=code,
                expires_at=timezone.now() + timedelta(minutes=5)  # 유효시간 5분
            )
            send_mail(
                'Your Verification Code',
                f'Your verification code is {code}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return JsonResponse({'sent': True})
        else:
            return JsonResponse({'sent': False, 'error': 'User with this email does not exist.'})
    return JsonResponse({'sent': False, 'error': 'Invalid request method.'})

def verify_email(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        code = request.POST.get('code')
        try :
            verification = EmailVerification.objects.get(user=user, verification_code=code)
            if verification.is_verified :
                return HttpResponse('This email is already verified')
            if timezone.now() > verification.expires_at:
                return HttpResponse("this verification code has expired.")
            
            verification.is_verified = True
            verification.save()
            login(request, user)
            return HttpResponse("Email verified and user logged in")
        except EmailVerification.DoesNotExist :
            return HttpResponse("Invalid verification code")
    return render(request, 'verify_email.html', {'user_id': user_id})
