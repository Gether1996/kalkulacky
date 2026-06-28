from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import datetime


class CustomUserManager(BaseUserManager):
    """Manager for custom user model with email as primary key."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with email and password."""
        if not email:
            raise ValueError('Email address is required')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with email as the primary key and source of truth.
    
    Fields:
    - email: Primary key, unique identifier
    - password: Hashed password
    - first_name: Optional first name
    - last_name: Optional last name
    - is_active: Boolean flag for account activation
    - is_staff: Boolean flag for admin access
    - is_superuser: Inherited from PermissionsMixin
    - date_joined: Timestamp of account creation
    - last_login: Inherited from AbstractBaseUser
    """
    
    email = models.EmailField(
        max_length=255,
        unique=True,
        primary_key=True,
        verbose_name='Email Address'
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Whether the user wants to receive reminder/notification emails (master switch).
    email_notifications = models.BooleanField(default=True)
    
    # OAuth fields
    oauth_provider = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text='OAuth provider (google, etc.)'
    )
    oauth_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='OAuth provider user ID'
    )
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email is already required as USERNAME_FIELD
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}".strip() or self.email
    
    def get_short_name(self):
        """Return the user's short name."""
        return self.first_name or self.email
