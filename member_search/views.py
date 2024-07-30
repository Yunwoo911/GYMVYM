from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.models import CustomUser
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import json

class SearchUserName(APIView):
    def get(self, request, username):
        users = CustomUser.objects.filter(username__icontains=username)
        user_data = [{'username': user.username, 'email': user.email, 'nfc_uid': user.nfc_uid} for user in users]
        return JsonResponse(user_data, safe=False, status=status.HTTP_200_OK)

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

# class IdentifyNFC(APIView):
#     @method_decorator(csrf_exempt)
#     def post(self, request):
#         try:
#             data = json.loads(request.body)
#             print("Request Data: ", data)  # 디버깅을 위해 요청 데이터 출력
#             nfc_uid = data.get('nfc_uid')
#             email = data.get('email')

#             if not nfc_uid:
#                 return Response({'error': 'NFC UID가 제공되지 않았습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            
#             if not email:
#                 return Response({'error': '이메일이 제공되지 않았습니다.'}, status=status.HTTP_400_BAD_REQUEST)

#             try:
#                 user = CustomUser.objects.get(email=email)
#                 user.nfc_uid = nfc_uid
#                 user.save()
#                 return Response({'status': 'success'}, status=status.HTTP_200_OK)
#             except CustomUser.DoesNotExist:
#                 return Response({'error': '해당 이메일을 가진 사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

#         except json.JSONDecodeError:
#             return Response({'error': '잘못된 JSON 형식입니다.'}, status=status.HTTP_400_BAD_REQUEST)