from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ('username','email','password','profile_image')


    def validate(self,data):

        email = data.get('email')
        if email and UserProfile.objects.filter(email=email).exists():
             raise serializers.ValidationError("User already registered.")
        
        profile_image = data.get('profile_image')
        if profile_image and profile_image.size > 10 * 1024 * 1024:  # 10 MB limit
            raise serializers.ValidationError("Profile image size exceeds the limit.")

        return data

    def create(self,validated_data):
        user = UserProfile.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password'],
            profile_image=validated_data.get('profile_image'),
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid credentials')

        data['user'] = user
        return data
        
    
    def get_token(self,user):
        print(user)
        refresh = RefreshToken.for_user(user)
        return {
            'refresh' : str(refresh),
            'access' : str(refresh.access_token),
        }