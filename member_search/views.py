from django.shortcuts import render, redirect
from .serializers import CustomUserSearchSerializers
from account.models import CustomUser
from rest_framework.views import APIView
import json
from django.http import JsonResponse
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

class SearchUserName(APIView):
    def get(self, request, username):
        users = CustomUser.objects.filter(username__icontains=username)
        user_data = [{'username': user.username, 'email': user.email, 'nfc_uid': user.nfc_uid} for user in users]
        return JsonResponse(user_data, safe=False, status=status.HTTP_200_OK)

@login_required
def search_member_view(request):
    return render(request, "search/search_member.html")

class nfc():
    pass

# user테이블에 nfc_uid 등록
@csrf_exempt
def register_nfc(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        nfc_uid = request.POST.get('nfc_uid')

        if not email or not nfc_uid:
            return JsonResponse({'error': 'Missing email or NFC UID'}, status=400)
        
        try:
            user = CustomUser.objects.get(email=email)
            user.nfc_uid = nfc_uid
            user.save()
            # 성공적으로 저장한 후 검색 페이지로 리디렉션
            return redirect('member_search:search_member')
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    
    return JsonResponse({'message': 'Invalid request'}, status=400)