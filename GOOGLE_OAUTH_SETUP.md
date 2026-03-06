# Google OAuth Setup Guide

## 1. Google Cloud Console Setup

### Krok 1: Vytvorenie projektu

1. Choďte na [Google Cloud Console](https://console.developers.google.com/)
2. Kliknite na "Select a project" → "New Project"
3. Zadajte názov projektu (napr. "Kalkulacky")
4. Kliknite "Create"

### Krok 2: Povoliť Google+ API

1. V ľavom menu choďte na "APIs & Services" → "Library"
2. Vyhľadajte "Google+ API"
3. Kliknite na "Google+ API"
4. Kliknite "Enable"

### Krok 3: Vytvoriť OAuth 2.0 credentials

1. V ľavom menu choďte na "APIs & Services" → "Credentials"
2. Kliknite "Create Credentials" → "OAuth client ID"
3. Ak sa zobrazí upozornenie o OAuth consent screen:
   - Kliknite "Configure Consent Screen"
   - Vyberte "External"
   - Vyplňte základné informácie:
     - App name: "Kalkulačky"
     - User support email: váš email
     - Developer contact: váš email
   - Kliknite "Save and Continue"
   - V "Scopes" pridajte:
     - .../auth/userinfo.email
     - .../auth/userinfo.profile
   - Kliknite "Save and Continue"
   - Pridajte test users (development)
   - Kliknite "Save and Continue"

4. Vráťte sa na "Credentials" a znova kliknite "Create Credentials" → "OAuth client ID"
5. Vyberte "Web application"
6. Zadajte názov (napr. "Kalkulacky Web Client")
7. Authorized JavaScript origins:
   ```
   http://localhost:4200
   http://localhost:8000
   ```
8. Authorized redirect URIs:
   ```
   http://localhost:4200/auth/callback
   http://localhost:8000/accounts/google/login/callback/
   ```
9. Kliknite "Create"
10. Skopírujte **Client ID** a **Client Secret**

YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com
YOUR_GOOGLE_CLIENT_SECRET

---

## 2. Backend Configuration

### Django Settings

Otvorte `django_calculators/django_calculators/settings.py` a updatujte:

```python
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'APP': {
            'client_id': 'YOUR_CLIENT_ID_HERE',
            'secret': 'YOUR_CLIENT_SECRET_HERE',
            'key': ''
        }
    }
}
```

### Environment Variables (Recommended)

Vytvorte `.env` súbor v `django_calculators/`:

```env
GOOGLE_OAUTH_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
```

Updatujte `settings.py`:

```python
from decouple import config

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': config('GOOGLE_OAUTH_CLIENT_ID', default=''),
            'secret': config('GOOGLE_OAUTH_CLIENT_SECRET', default=''),
            'key': ''
        }
    }
}
```

---

## 3. Frontend Configuration

### Inštalácia Google Sign-In SDK

V `frontend/` adresári spustite:

```bash
npm install @types/gapi @types/gapi.auth2
```

### Pridajte Google SDK do index.html

Otvorte `frontend/src/index.html` a pridajte:

```html
<head>
  ...
  <script src="https://accounts.google.com/gsi/client" async defer></script>
  <meta name="google-signin-client_id" content="YOUR_CLIENT_ID.apps.googleusercontent.com">
</head>
```

### Updatujte Login Component

V `frontend/src/app/components/login/login.ts`:

```typescript
// Add to constructor or ngOnInit
ngOnInit() {
  this.loadGoogleScript();
}

private loadGoogleScript() {
  // @ts-ignore
  google.accounts.id.initialize({
    client_id: 'YOUR_CLIENT_ID.apps.googleusercontent.com',
    callback: this.handleGoogleResponse.bind(this)
  });

  // @ts-ignore
  google.accounts.id.renderButton(
    document.getElementById('googleSignInButton'),
    { 
      theme: 'outline', 
      size: 'large',
      text: 'signin_with',
      locale: 'sk'
    }
  );
}

private handleGoogleResponse(response: any) {
  const idToken = response.credential;
  
  this.authService.googleAuth(idToken).subscribe({
    next: () => {
      this.router.navigate([this.returnUrl]);
    },
    error: (error) => {
      this.errorMessage = 'Google prihlásenie zlyhalo';
      console.error('Google auth error:', error);
    }
  });
}
```

Updatujte template:

```html
<!-- Replace existing Google button with -->
<div id="googleSignInButton"></div>
```

---

## 4. Testing OAuth Flow

### Backend Test

1. Spustite Django server:
```bash
cd django_calculators
python manage.py runserver
```

2. Test endpoint s Google ID token:
```bash
curl -X POST http://localhost:8000/api/auth/google/ \
  -H "Content-Type: application/json" \
  -d '{"token":"GOOGLE_ID_TOKEN_HERE"}'
```

### Frontend Test

1. Spustite Angular:
```bash
cd frontend
ng serve
```

2. Otvorte browser: http://localhost:4200/login
3. Kliknite na "Sign in with Google"
4. Vyberte Google účet
5. Povoľte prístup
6. Malo by vás automaticky prihlásiť a presmerovať

---

## 5. Production Setup

### Google Cloud Console

1. Zmeňte OAuth consent screen na "Production"
2. Updatujte Authorized origins:
   ```
   https://yourdomain.com
   ```
3. Updatujte Authorized redirect URIs:
   ```
   https://yourdomain.com/auth/callback
   https://yourdomain.com/accounts/google/login/callback/
   ```

### Django Production Settings

```python
# Use environment variables
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.environ.get('GOOGLE_OAUTH_CLIENT_ID'),
            'secret': os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET'),
        }
    }
}

# SSL/HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Angular Production

Updatujte `environment.prod.ts`:

```typescript
export const environment = {
  production: true,
  apiUrl: 'https://yourdomain.com/api',
  googleClientId: 'YOUR_PRODUCTION_CLIENT_ID'
};
```

---

## 6. Troubleshooting

### Error: "redirect_uri_mismatch"

**Riešenie:**
- Skontrolujte, že redirect URI v Google Console presne sedí s URI v aplikácii
- Musí byť presná zhoda (http vs https, port, trailing slash)

### Error: "Invalid token"

**Riešenie:**
- Token je exspirovaný (platnosť 1 hodina)
- Client ID nesedí s tokenom
- Skontrolujte konzolu pre podrobnosti

### Error: "Access blocked: This app's request is invalid"

**Riešenie:**
- OAuth consent screen nie je nakonfigurovaný
- Chýbajú required scopes
- App nie je verified (development mode má limit 100 users)

### User nemá email po OAuth login

**Riešenie:**
- Pridajte email scope do Google OAuth settings
- Skontrolujte, že SOCIALACCOUNT_QUERY_EMAIL = True

---

## 7. Security Best Practices

1. **Never commit secrets to git**
   ```bash
   # Add to .gitignore
   .env
   *.env
   ```

2. **Use environment variables in production**
   ```python
   client_id = os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
   ```

3. **Verify token on backend**
   - Never trust frontend validation
   - Always verify ID token with Google

4. **Use HTTPS in production**
   - Google OAuth requires HTTPS for production
   - Use Let's Encrypt for free SSL

5. **Implement rate limiting**
   - Protect against brute force
   - Use django-ratelimit

6. **Log OAuth attempts**
   - Monitor failed attempts
   - Alert on suspicious activity

---

## 8. Alternative: Google OAuth with Popup

Ak chcete použiť popup namiesto redirect:

```typescript
loginWithGoogle() {
  // @ts-ignore
  google.accounts.id.prompt((notification: any) => {
    if (notification.isNotDisplayed()) {
      console.log('Google One Tap not displayed');
    } else if (notification.isSkippedMoment()) {
      console.log('Google One Tap skipped');
    }
  });
}
```

---

## Resources

- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Django Allauth Documentation](https://django-allauth.readthedocs.io/)
- [Google Sign-In JavaScript API](https://developers.google.com/identity/gsi/web)
- [Angular HTTP Interceptors](https://angular.io/guide/http#intercepting-requests-and-responses)
