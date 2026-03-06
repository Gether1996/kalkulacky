from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import authenticate, login, logout
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.conf import settings

from .models import User
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    GoogleAuthSerializer
)


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    
    POST /api/auth/register/
    Body: {
        "email": "user@example.com",
        "password": "securepassword123",
        "password_confirm": "securepassword123",
        "first_name": "John",  // optional
        "last_name": "Doe"  // optional
    }
    
    Response: {
        "user": {...},
        "access": "jwt_access_token",
        "refresh": "jwt_refresh_token"
    }
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    API endpoint for user login.
    
    POST /api/auth/login/
    Body: {
        "email": "user@example.com",
        "password": "securepassword123"
    }
    
    Response: {
        "user": {...},
        "access": "jwt_access_token",
        "refresh": "jwt_refresh_token"
    }
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        login(request, user)
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    API endpoint for user logout.
    
    POST /api/auth/logout/
    Body: {
        "refresh": "jwt_refresh_token"
    }
    
    Response: {
        "message": "Logout successful"
    }
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            logout(request)
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint to retrieve or update user profile.
    
    GET /api/auth/profile/
    Response: {
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        ...
    }
    
    PATCH/PUT /api/auth/profile/
    Body: {
        "first_name": "John",
        "last_name": "Doe"
    }
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    """
    API endpoint for changing password.
    
    POST /api/auth/change-password/
    Body: {
        "old_password": "currentpassword",
        "new_password": "newpassword123",
        "new_password_confirm": "newpassword123"
    }
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        # Set new password
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'message': 'Password changed successfully'
        }, status=status.HTTP_200_OK)


class GoogleAuthView(APIView):
    """
    API endpoint for Google OAuth authentication.
    
    POST /api/auth/google/
    Body: {
        "token": "google_id_token"
    }
    
    Response: {
        "user": {...},
        "access": "jwt_access_token",
        "refresh": "jwt_refresh_token"
    }
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data['token']
        
        try:
            # Verify the Google token
            # Note: You need to set GOOGLE_OAUTH_CLIENT_ID in settings
            client_id = settings.SOCIALACCOUNT_PROVIDERS.get('google', {}).get('APP', {}).get('client_id')
            
            if not client_id:
                return Response({
                    'error': 'Google OAuth is not configured'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            idinfo = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                client_id
            )
            
            # Get user info from Google token
            email = idinfo.get('email')
            first_name = idinfo.get('given_name', '')
            last_name = idinfo.get('family_name', '')
            google_id = idinfo.get('sub')
            
            if not email:
                return Response({
                    'error': 'Email not provided by Google'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get or create user
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'oauth_provider': 'google',
                    'oauth_id': google_id,
                }
            )
            
            # Update OAuth info if user already exists
            if not created:
                if not user.oauth_provider:
                    user.oauth_provider = 'google'
                    user.oauth_id = google_id
                    user.save()
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': UserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'created': created
            }, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({
                'error': 'Invalid Google token'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CheckAuthView(APIView):
    """
    API endpoint to check if user is authenticated.
    
    GET /api/auth/check/
    Response: {
        "authenticated": true,
        "user": {...}
    }
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        if request.user.is_authenticated:
            return Response({
                'authenticated': True,
                'user': UserSerializer(request.user).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'authenticated': False,
                'user': None
            }, status=status.HTTP_200_OK)
