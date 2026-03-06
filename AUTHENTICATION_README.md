# Authentication & Authorization System

## Prehľad

Kompletný autentifikačný systém pre Django + Angular aplikáciu s podporou:
- Email + heslo registrácia/prihlásenie
- JWT token autentifikácia  
- Google OAuth2 integrácia
- User profil management
- Password change funkčnosť

---

## Backend (Django)

### 1. Custom User Model

**Súbor:** `django_calculators/users/models.py`

- Email ako primary key a username field
- PermissionsMixin pre Django permissions
- OAuth fields (provider, oauth_id)
- CustomUserManager pre vytáranie users

**Polia:**
- `email` (PK) - Unique email address
- `password` - Hashed password
- `first_name`, `last_name` - Optional
- `is_active`, `is_staff`, `is_superuser` - Permissions
- `oauth_provider`, `oauth_id` - OAuth info
- `date_joined`, `last_login` - Timestamps

### 2. API Endpoints

**Base URL:** `http://localhost:8000/api/auth/`

#### Register
```
POST /api/auth/register/
Body: {
  "email": "user@example.com",
  "password": "password123",
  "password_confirm": "password123",
  "first_name": "John",  // optional
  "last_name": "Doe"     // optional
}
Response: {
  "user": {...},
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token"
}
```

#### Login
```
POST /api/auth/login/
Body: {
  "email": "user@example.com",
  "password": "password123"
}
Response: {
  "user": {...},
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token"
}
```

#### Logout
```
POST /api/auth/logout/
Headers: Authorization: Bearer <access_token>
Body: {
  "refresh": "jwt_refresh_token"
}
```

#### Get/Update Profile
```
GET /api/auth/profile/
Headers: Authorization: Bearer <access_token>

PATCH /api/auth/profile/
Headers: Authorization: Bearer <access_token>
Body: {
  "first_name": "John",
  "last_name": "Doe"
}
```

#### Change Password
```
POST /api/auth/change-password/
Headers: Authorization: Bearer <access_token>
Body: {
  "old_password": "oldpassword",
  "new_password": "newpassword123",
  "new_password_confirm": "newpassword123"
}
```

#### Google OAuth
```
POST /api/auth/google/
Body: {
  "token": "google_id_token"
}
Response: {
  "user": {...},
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token",
  "created": true/false
}
```

#### Check Auth Status
```
GET /api/auth/check/
Response: {
  "authenticated": true,
  "user": {...}
}
```

#### Refresh Token
```
POST /api/auth/token/refresh/
Body: {
  "refresh": "jwt_refresh_token"
}
Response: {
  "access": "new_jwt_access_token",
  "refresh": "new_jwt_refresh_token"  // if ROTATE_REFRESH_TOKENS=True
}
```

### 3. JWT Configuration

**Súbor:** `django_calculators/django_calculators/settings.py`

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'USER_ID_FIELD': 'email',
}
```

### 4. Google OAuth Setup

1. Získajte credentials z [Google Cloud Console](https://console.developers.google.com/)
2. Vytvorte OAuth 2.0 Client ID
3. Pridajte do settings.py:

```python
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': 'your-client-id',
            'secret': 'your-client-secret',
        }
    }
}
```

### 5. Database Migration

```bash
cd django_calculators
python manage.py makemigrations users
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
# Email: admin@example.com
# Password: ***
```

---

## Frontend (Angular)

### 1. Auth Service

**Súbor:** `frontend/src/app/services/auth.service.ts`

Centrálny service pre autentifikáciu s nasledujúcimi metódami:

- `register(data)` - Registrácia nového usera
- `login(data)` - Prihlásenie
- `logout()` - Odhlásenie
- `googleAuth(token)` - Google OAuth
- `getProfile()` - Získanie user profilu
- `updateProfile(data)` - Update profilu
- `changePassword(data)` - Zmena hesla
- `refreshToken()` - Refresh JWT tokenu
- `checkAuthStatus()` - Kontrola auth statusu

**Signals & Observables:**
- `currentUser$` - Observable pre aktuálneho usera
- `isAuthenticated` - Signal pre auth status

### 2. HTTP Interceptor

**Súbor:** `frontend/src/app/interceptors/auth.interceptor.ts`

Automaticky pridáva JWT token do HTTP requestov a refreshuje token pri 401 erroroch.

### 3. Route Guards

**Súbor:** `frontend/src/app/guards/auth.guard.ts`

- `authGuard` - Ochrana routes pre prihlásených userov
- `guestGuard` - Ochrana routes pre neprihlásených userov

### 4. Components

#### Login Component
**Path:** `/login`
**Súbory:** `frontend/src/app/components/login/`
- Email + password prihlásenie
- Google OAuth button
- Link na registráciu
- Error handling

#### Register Component
**Path:** `/register`
**Súbory:** `frontend/src/app/components/register/`
- Email + password registrácia
- First name, last name (optional)
- Password confirmation validation
- Link na login

#### User Profile Component
**Path:** `/profile`
**Súbory:** `frontend/src/app/components/user-profile/`
- Zobrazenie user info
- Update first/last name
- Change password (pre non-OAuth users)
- Logout button

### 5. App Configuration

Pridajte do `app.config.ts`:

```typescript
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { authInterceptor } from './interceptors/auth.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(
      withInterceptors([authInterceptor])
    ),
    // ... other providers
  ]
};
```

### 6. Routes Configuration

Pridajte do `app.routes.ts`:

```typescript
import { Routes } from '@angular/router';
import { authGuard, guestGuard } from './guards/auth.guard';
import { Login } from './components/login/login';
import { Register } from './components/register/register';
import { UserProfile } from './components/user-profile/user-profile';

export const routes: Routes = [
  { path: 'login', component: Login, canActivate: [guestGuard] },
  { path: 'register', component: Register, canActivate: [guestGuard] },
  { path: 'profile', component: UserProfile, canActivate: [authGuard] },
  // ... other routes
];
```

### 7. Using Auth in Components

```typescript
import { Component } from '@angular/core';
import { AuthService } from './services/auth.service';

@Component({...})
export class MyComponent {
  constructor(public authService: AuthService) {}
  
  ngOnInit() {
    // Subscribe to current user
    this.authService.currentUser$.subscribe(user => {
      console.log('Current user:', user);
    });
    
    // Check if authenticated
    if (this.authService.isAuthenticated()) {
      console.log('User is authenticated');
    }
  }
  
  logout() {
    this.authService.logout().subscribe();
  }
}
```

### 8. Using Auth in Templates

```html
<!-- Show content only for authenticated users -->
<div *ngIf="authService.isAuthenticated()">
  <p>Welcome, {{ (authService.currentUser$ | async)?.email }}</p>
  <button (click)="logout()">Logout</button>
</div>

<!-- Show content only for guests -->
<div *ngIf="!authService.isAuthenticated()">
  <a routerLink="/login">Login</a>
  <a routerLink="/register">Register</a>
</div>
```

---

## Testing

### Backend Testing

1. Start Django server:
```bash
cd django_calculators
python manage.py runserver
```

2. Test endpoints s Postman alebo curl:
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123","password_confirm":"testpass123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'

# Get Profile (replace TOKEN)
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer TOKEN"
```

### Frontend Testing

1. Start Angular dev server:
```bash
cd frontend
ng serve
```

2. Otvorte browser: http://localhost:4200
3. Test flows:
   - Registrácia nového usera
   - Prihlásenie
   - Zobrazenie profilu
   - Update profilu
   - Zmena hesla
   - Odhlásenie

---

## Security Notes

### Production Checklist

1. **Django settings.py:**
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Use strong `SECRET_KEY`
   - Configure real email backend (SMTP)
   - Enable HTTPS
   - Configure CORS properly

2. **JWT Tokens:**
   - Store access token in memory (not localStorage for XSS protection)
   - Store refresh token in httpOnly cookie
   - Use short-lived access tokens (1 hour)
   - Implement token rotation

3. **Google OAuth:**
   - Never commit CLIENT_SECRET to git
   - Use environment variables
   - Restrict OAuth redirect URIs
   - Verify token on backend

4. **Password Security:**
   - Django default: PBKDF2 with SHA256
   - Enforce password complexity
   - Consider adding 2FA

5. **HTTPS:**
   - Always use HTTPS in production
   - Enable HSTS
   - Secure cookies

---

## Troubleshooting

### Backend Issues

**Error: "No module named 'rest_framework_simplejwt'"**
```bash
pip install djangorestframework-simplejwt
```

**Error: "No module named 'allauth'"**
```bash
pip install django-allauth
```

**Error: "auth.User.groups: (fields.E304)"**
- Remove old migrations
- Run `python manage.py makemigrations users --empty`
- Run `python manage.py migrate`

### Frontend Issues

**Error: "Cannot find module '@angular/common/http'"**
```bash
npm install
```

**CORS Error**
- Check Django CORS settings
- Ensure `http://localhost:4200` is in `CORS_ALLOWED_ORIGINS`

**Token not sent in requests**
- Check if interceptor is properly configured
- Verify token is stored in localStorage
- Check browser console for errors

---

## Next Steps

1. ✅ Basic authentication implemented
2. ⬜ Add email verification
3. ⬜ Add password reset functionality
4. ⬜ Add 2FA (Two-Factor Authentication)
5. ⬜ Add social auth providers (Facebook, GitHub)
6. ⬜ Add refresh token rotation
7. ⬜ Add rate limiting
8. ⬜ Add session management (view active sessions)
9. ⬜ Add user activity logging
10. ⬜ Add admin panel for user management

---

## File Structure

```
django_calculators/
├── users/                          # Auth app
│   ├── models.py                   # Custom User model
│   ├── serializers.py              # Auth serializers
│   ├── views.py                    # Auth views/endpoints
│   ├── urls.py                     # Auth URLs
│   ├── admin.py                    # Admin interface
│   └── migrations/
├── django_calculators/
│   ├── settings.py                 # JWT, OAuth config
│   └── urls.py                     # Include auth URLs
└── requirements.txt                # Auth dependencies

frontend/
├── src/app/
│   ├── models/
│   │   └── auth.models.ts          # Auth interfaces
│   ├── services/
│   │   └── auth.service.ts         # Auth service
│   ├── guards/
│   │   └── auth.guard.ts           # Route guards
│   ├── interceptors/
│   │   └── auth.interceptor.ts     # HTTP interceptor
│   └── components/
│       ├── login/                  # Login component
│       ├── register/               # Register component
│       └── user-profile/           # Profile component
└── package.json
```

---

## Dependencies

### Backend (requirements.txt)
```
Django==5.0
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.1
django-allauth==0.57.0
google-auth==2.27.0
google-auth-oauthlib==1.2.0
google-auth-httplib2==0.2.0
django-cors-headers==4.3.1
```

### Frontend (package.json)
```json
{
  "dependencies": {
    "@angular/common": "^18.0.0",
    "@angular/core": "^18.0.0",
    "@angular/forms": "^18.0.0",
    "@angular/router": "^18.0.0",
    "rxjs": "^7.8.0"
  }
}
```
