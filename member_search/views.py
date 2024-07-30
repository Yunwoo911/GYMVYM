from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.models import CustomUser
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

def search_member_view(request):
    return render(request, "search/search_member.html")

class SearchUserName(APIView):
    def get(self, request, username):
        users = CustomUser.objects.filter(username__icontains=username)
        user_data = [{'username': user.username, 'email': user.email, 'nfc_uid': user.nfc_uid} for user in users]
        return JsonResponse(user_data, safe=False, status=status.HTTP_200_OK)

@csrf_exempt
def register_nfc(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        nfc_uid = data.get('nfc_uid')

        if not email or not nfc_uid:
            return JsonResponse({'error': 'Missing email or NFC UID'}, status=400)
        
        try:
            user = CustomUser.objects.get(email=email)
            user.nfc_uid = nfc_uid
            user.save()
            return JsonResponse({'status': 'success'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    
    return JsonResponse({'message': 'Invalid request'}, status=400)
