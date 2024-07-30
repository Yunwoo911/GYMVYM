from rest_framework import serializers
from account.models import CustomUser

class CustomUserSearchSerializers(serializers.ModelSerializer) :
    class Meta :
        model = CustomUser
        fields =['username']

class NFCUIDSerializer(serializers.Serializer):
    nfc_uid = serializers.CharField(max_length=255)