from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer,LoginSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class SignupView(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data , context ={'request':request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = serializer.get_token(user)
            return Response(token,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
