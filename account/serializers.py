from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer) : 
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta :
        model = CustomUser
        fields = ('user_id', 'username', 'password', 'password2', 'email', 'usertype', 'nickname', 'image', 'birth', 'gender', 'is_superuser', 'user_image')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password" : "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        user = CustomUser.objects.create(
            user_id=validated_data['user_id'],
            user_name=validated_data['username'],
            email=validated_data['email'],
            usertype=validated_data['usertype'],
            nickname=validated_data['nickname'],
            birth=validated_data['birth'],
            gender=validated_data['gender'],
            is_superuser=validated_data['is_superuser'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
    
class UserSerializerNoIMG(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('user_id', 'username', 'password', 'password2', 'email', 'usertype', 'nickname', 'image', 'birth', 'gender', 'is_superuser')
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid login credentials")
        else:
            raise serializers.ValidationError("Must include email and password")
        
        attrs['user'] = user
        return attrs