from django.contrib.auth.password_validation import validate_password
from .models import CustomUser
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())], # 이메일에 대한 중복 검증
    )
    password = serializers.CharField(
        write_only =True,
        required = True,
        validators =[validate_password],
    )
    password2 = serializers.CharField(
        write_only =True,
        required = True,
    )
    phone1 = serializers.CharField(
        required=True,
        max_length = 3,
    )
    phone2 = serializers.CharField(
        required=True,
        max_length = 4,
    )
    phone3 = serializers.CharField(
        required=True,
        max_length = 4,
    )

    class Meta :
        model = CustomUser
        fields = ['user_image', 'username', 'password', 'password2', 'email', 'usertype', 'phone1', 'phone2', 'phone3', 'birth', 'address', 'detail_address', 'nickname', 'gender', 'is_superuser']
    
    def validate(self, data): # password과 password2의 일치 여부 확인
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        
        return data

    def create(self, validated_data):
        phone1 = validated_data['phone1']
        phone2 = validated_data['phone2']
        phone3 = validated_data['phone3']

        # CREATE 요청에 대해 create 메서드를 오버라이딩하여, 유저를 생성하고 토큰도 생성하게 해준다.
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone1 = phone1,
            phone2 = phone2,
            phone3 = phone3,
            birth=validated_data['birth'],
            address=validated_data['address'],
            detail_address=validated_data['detail_address'],
            nickname=validated_data['nickname'],
            gender=validated_data['gender'],
            is_superuser=validated_data['is_superuser'],
            user_image= validated_data['user_image'],
        )

        user.set_password(validated_data['password'])
        user.save()

        token = Token.objects.create(user=user)

        return user
    
class LoginSerializer(serializers.Serializer) :
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user :
            token = Token.objects.get(user=user)
            return token
        raise serializers.ValidationError({"error": "Unable to log in with provided credentials."})
    
class NFCSerializers(serializers.Serializer) :
    nfc_uid = serializers.CharField(required=True) 


    
    

