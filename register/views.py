from rest_framework import generics 
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer, StudentDetailsSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import CustomUser, StudentDetails
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User



class RegisterView(APIView): 
    
    permission_classes = [AllowAny,] 

    def post(self, request):
        data = request.data.copy()
        if not request.user.is_authenticated:
            if 'is_staff' in data:
                return Response(
                    {"error": "'is_staff' field cannot be provided for unauthenticated users."})
            data['is_staff'] = False
            print(data['is_staff'], "not auth")
        if request.user.is_authenticated and request.user.is_superuser:
            if 'is_staff' in data:
                data['is_staff'] = data.get('is_staff')
                print(data['is_staff'], "auth tut")
            else:
                data['is_staff'] = False
                print(data['is_staff'], "auth std")
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            if 'is_staff' in data:
                user.is_staff = data['is_staff']
                user.save() 
            return Response(
                {"message": "User created successfully", "data": serializer.data}
            )
        return Response(serializer.errors)


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