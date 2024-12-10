from rest_framework import generics 
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response



class RegisterView(generics.CreateAPIView): 
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,) 
    serializer_class = RegisterSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CheckSessionView(APIView):
    def get(self, request, *args, **kwargs):
        session_data = {
            'refresh_token': request.session.get('refresh_token'),
            'access_token': request.session.get('access_token'),
            'user_email': request.session.get('user_email'),
        }
        return Response(session_data)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = request.user

        user_data = {
            "name": user.get_full_name(),
            "email": user.email,
            "mobile": user.mobile,
        }
        return Response(user_data)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        request.session.flush()
        return Response({"message": "logged out"})