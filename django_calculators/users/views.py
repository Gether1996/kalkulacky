from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import authenticate, login, logout
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.conf import settings

import logging
from .models import User
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    GoogleAuthSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)

audit_logger = logging.getLogger('audit')


def _auth_client_ip(request):
    """Best-effort client IP (honours a single proxy hop)."""
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def log_auth_event(request, event, email='', user=None):
    """Record an auth/audit event to the DB (AuthEvent) and logs/audit.log."""
    try:
        from calculators.models import AuthEvent
        ip = _auth_client_ip(request)
        resolved_email = email or getattr(user, 'email', '') or ''
        AuthEvent.objects.create(
            event=event, email=resolved_email, user=user,
            ip_address=ip, user_agent=request.META.get('HTTP_USER_AGENT', '')[:300],
        )
        # Sanitize attacker-controlled email before it reaches the log line —
        # strip CR/LF so a crafted value can't forge fake audit-log entries.
        safe_email = (resolved_email or '-').replace('\n', ' ').replace('\r', ' ')[:200]
        audit_logger.info('auth.%s email=%s ip=%s', event, safe_email, ip or '-')
    except Exception as e:  # never let logging break auth
        audit_logger.error('auth-event log failed (%s): %s', event, e)


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
    throttle_scope = 'register'  # cap account-creation flooding (ScopedRateThrottle)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        log_auth_event(request, 'register', user=user)

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
    throttle_scope = 'login'  # brute-force protection (per IP)

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            log_auth_event(request, 'login_failed', email=request.data.get('email', ''))
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']
        login(request, user)
        log_auth_event(request, 'login', user=user)

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
            user = request.user if getattr(request.user, 'is_authenticated', False) else None
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            log_auth_event(request, 'logout', user=user)
            logout(request)
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            audit_logger.exception('logout error: %s', e)
            return Response({
                'error': 'Odhlásenie zlyhalo. Skúste to prosím znova.'
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


class DeleteAccountView(APIView):
    """
    GDPR right to erasure — permanently delete the logged-in user's account and
    all related data (saved calculations, reminders cascade via FK).

    DELETE /api/auth/delete-account/
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        user = request.user
        user_email = user.email
        log_auth_event(request, 'account_deleted', user=user)

        # GDPR erasure: PII in these tables is keyed by an email/IP string, not a
        # FK, so it does NOT cascade with user.delete(). Purge/anonymize it here.
        from calculators.models import Lead, DataReport, AuthEvent, SavedCalculation
        Lead.objects.filter(email__iexact=user_email).delete()
        DataReport.objects.filter(reporter_email__iexact=user_email).delete()
        # Anonymous saves (no FK) that carry the user's email don't cascade — purge them too.
        SavedCalculation.objects.filter(user__isnull=True, email__iexact=user_email).delete()
        # Keep the audit trail rows but strip the personal data from them.
        AuthEvent.objects.filter(email__iexact=user_email).update(
            email='', ip_address=None, user_agent='',
        )

        user.delete()
        return Response(
            {'message': 'Váš účet a súvisiace údaje boli natrvalo odstránené.'},
            status=status.HTTP_200_OK,
        )


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


class ForgotPasswordView(APIView):
    """
    Request a password-reset email.

    POST /api/auth/forgot-password/  Body: { "email": "..." }
    Always returns success (does not reveal whether the email exists). Emails a
    reset link to the frontend /reset-password page. Needs SMTP configured to
    actually deliver (console backend in dev).
    """
    permission_classes = [permissions.AllowAny]
    throttle_scope = 'forgot_password'

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        user = User.objects.filter(email__iexact=email, is_active=True).first()
        if user and not user.oauth_provider:
            from django.contrib.auth.tokens import default_token_generator
            from django.utils.http import urlsafe_base64_encode
            from django.utils.encoding import force_bytes
            from django.core.mail import send_mail

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            base = getattr(settings, 'FRONTEND_URL', 'https://kalkulacky.sk')
            reset_link = f"{base}/reset-password?uid={uid}&token={token}"
            try:
                send_mail(
                    'Obnovenie hesla – Kalkulačky.sk',
                    f'Pre obnovenie hesla kliknite na odkaz (platí 24 hodín):\n\n{reset_link}\n\n'
                    f'Ak ste o obnovenie nežiadali, tento e-mail ignorujte.',
                    getattr(settings, 'DEFAULT_FROM_EMAIL', None),
                    [user.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Password reset email failed: {e}")

        return Response(
            {'message': 'Ak účet s týmto e-mailom existuje, poslali sme naň odkaz na obnovenie hesla.'},
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(APIView):
    """
    Set a new password using the emailed uid + token.

    POST /api/auth/reset-password/
    Body: { "uid", "token", "new_password", "new_password_confirm" }
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.http import urlsafe_base64_decode
        from django.utils.encoding import force_str

        try:
            uid = force_str(urlsafe_base64_decode(serializer.validated_data['uid']))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            user = None

        if user is None or not default_token_generator.check_token(
            user, serializer.validated_data['token']
        ):
            return Response(
                {'error': 'Odkaz na obnovenie hesla je neplatný alebo expiroval.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        log_auth_event(request, 'password_reset', user=user)
        return Response({'message': 'Heslo bolo úspešne zmenené. Môžete sa prihlásiť.'},
                        status=status.HTTP_200_OK)


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
            
            log_auth_event(request, 'register' if created else 'google_login', user=user)

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
            # Log the real error server-side; don't leak internals to the client.
            audit_logger.exception('google-auth error: %s', e)
            return Response({
                'error': 'Prihlásenie cez Google zlyhalo. Skúste to prosím neskôr.'
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
