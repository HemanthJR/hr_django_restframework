from rest_framework import serializers 
from django.contrib.auth.models import User
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()
class RegisterSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = CustomUser 
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'dob', 'mobile'] 
        extra_kwargs = { 
            'password': {'write_only': True},
            } 
    
    def create(self, validated_data): 
        user = CustomUser.objects.create_user( 
            username=validated_data['email'], 
            email=validated_data['email'], 
            password=validated_data['password'], 
            first_name=validated_data['first_name'], 
            last_name=validated_data['last_name'], 
            dob=validated_data['dob'], 
            mobile=validated_data['mobile'] ) 
        return user
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs): 
        email = attrs.get('email') 
        password = attrs.get('password')

        # print(attrs)
        user = authenticate(request=self.context.get('request'), email=email, password=password)


        if user is None: 
            raise serializers.ValidationError('Invalid email or password')
        
        refresh = self.get_token(user)

        request = self.context.get('request')
        if request and hasattr(request, 'session'):
            request.session['refresh_token'] = str(refresh)
            request.session['access_token'] = str(refresh.access_token)
            request.session['user_email'] = email

        data = { 
            'refresh': str(refresh), 
            'access': str(refresh.access_token), 
            'user':{
                user.get_full_name(),
                user.email
            }
        }

        return data