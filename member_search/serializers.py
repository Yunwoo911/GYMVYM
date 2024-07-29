from rest_framework import serializers
from account.models import CustomUser

class CustomUserSearchSerializers(serializers.ModelSerializer) :
    class Meta :
        model = CustomUser
        fields =['username']