from django.shortcuts import render
from .serializers import CustomUserSearchSerializers
from account.models import CustomUser
from rest_framework.views import APIView

# Create your views here.
class SearchUserName(APIView):
    def get(self, request, username):
        users = CustomUser.objects.filter(username=username)

def search_memeber_view(request):
    return render(request, "search_memeber.html")

class nfc():
    pass