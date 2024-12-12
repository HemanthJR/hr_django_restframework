from django.urls import path
from .views import (
    RegisterView, CustomTokenObtainPairView, LogoutView,
    CheckSessionView, UserProfileView
)
from rest_framework_simplejwt.views import ( 
    TokenObtainPairView, 
    TokenRefreshView, 
    )

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'), 
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('logout/', LogoutView.as_view(), name='logout_view'),
    path('protected/', CheckSessionView.as_view(), name='protected'),
    path('profile/', UserProfileView.as_view(), name="profile"),
]