from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .forms import SignupForm, ProfileForm
from .models import CustomUser
from .serializers import UserSerializerNoIMG, UserSerializer, LoginSerializer

@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.username,
        'email': request.user.email,
        'user_image': request.user.get_userimage(),
        'phone_number': request.user.phone_number,
        'address': request.user.address,
        'detail_address': request.user.detail_address,
        'usertype': request.user.usertype,
        'nickname': request.user.nickname,
        'birth': request.user.birth,
        'gender': request.user.gender
    })

@api_view(['GET'])
def me_noimg(request):
    serializer = UserSerializerNoIMG(request.user)
    return JsonResponse(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def editprofile(request):
    user = request.user
    user_name = request.data.get('username')

    if CustomUser.objects.exclude(id=user.id).filter(user_name=user_name).exists():
        return JsonResponse({'message': 'nickname already exists'})
    else:
        form = ProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()

        serializer = UserSerializer(user)
        
        return JsonResponse({'message': 'information updated', 'user': serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def editpassword(request):
    user = request.user
    
    form = PasswordChangeForm(data=request.POST, user=user)

    if form.is_valid():
        form.save()
        return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'message': form.errors.as_json()}, safe=False)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return JsonResponse({'message': 'success'}, status=200)
        return JsonResponse({'errors': serializer.errors}, status=400)
    return render(request, 'login.html')
