from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils.deprecation import MiddlewareMixin

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self,request):
        jwt_authenticator = JWTAuthentication()
        try:
            result = jwt_authenticator.authenticate(request)
            if result is not None:
                user, validated_token = result
                request.user = user
            else:
                request.user = None
        except AuthenticationFailed:
            request.user = None
            return Response({'error': 'Authentication credentials were not provided or are invalid.'}, status=401)
        
