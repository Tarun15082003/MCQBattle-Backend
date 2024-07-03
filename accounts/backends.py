from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import AuthenticationFailed

class UserDetailsBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed('No user found with this email.')

        if user.check_password(password):
            return user

        raise AuthenticationFailed('Invalid password.')

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
