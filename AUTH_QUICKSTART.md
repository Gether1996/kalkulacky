# Authentication System - Quick Start

## 🚀 Rýchly štart (Development)

### 1. Inštalácia závislostí

```bash
# Backend
cd django_calculators
pip install -r requirements.txt

# Frontend (ak potrebujete)
cd ../frontend
npm install
```

### 2. Databázové migrácie

```bash
cd django_calculators
python manage.py makemigrations users
python manage.py migrate
```

### 3. Vytvorenie superusera

```bash
python manage.py createsuperuser
# Email: admin@example.com
# Password: (zadajte heslo)
```

### 4. Spustenie servera

```bash
# Backend
python manage.py runserver

# Frontend (v inom termináli)
cd ../frontend
ng serve
```

### 5. Test aplikácie

1. Otvorte browser: http://localhost:4200
2. Kliknite na "Register" alebo choďte na http://localhost:4200/register
3. Registrujte nový účet
4. Po úspešnej registrácii by ste mali byť automaticky prihlásený
5. Choďte na http://localhost:4200/profile pre profil

---

## 📝 Základné použitie

### Backend API Endpoints

| Metóda | Endpoint | Popis |
|--------|----------|-------|
| POST | `/api/auth/register/` | Registrácia |
| POST | `/api/auth/login/` | Prihlásenie |
| POST | `/api/auth/logout/` | Odhlásenie |
| GET | `/api/auth/profile/` | Získanie profilu |
| PATCH | `/api/auth/profile/` | Update profilu |
| POST | `/api/auth/change-password/` | Zmena hesla |
| POST | `/api/auth/google/` | Google OAuth |
| POST | `/api/auth/token/refresh/` | Refresh JWT token |
| GET | `/api/auth/check/` | Kontrola auth statusu |

### Frontend Routes

| Route | Komponent | Guard | Popis |
|-------|-----------|-------|-------|
| `/login` | LoginComponent | guestGuard | Prihlásenie |
| `/register` | RegisterComponent | guestGuard | Registrácia |
| `/profile` | UserProfileComponent | authGuard | User profil |

### Použitie v komponentoch

```typescript
import { AuthService } from './services/auth.service';

export class MyComponent {
  constructor(public authService: AuthService) {}
  
  ngOnInit() {
    // Check if user is authenticated
    if (this.authService.isAuthenticated()) {
      console.log('User is logged in');
    }
    
    // Get current user
    this.authService.currentUser$.subscribe(user => {
      if (user) {
        console.log('Email:', user.email);
      }
    });
  }
}
```

### Použitie v templates

```html
<!-- Zobraz pre prihlásených -->
<div *ngIf="authService.isAuthenticated()">
  <p>Vitaj, {{ (authService.currentUser$ | async)?.email }}</p>
</div>

<!-- Zobraz pre neprihlásených -->
<div *ngIf="!authService.isAuthenticated()">
  <a routerLink="/login">Prihlásiť sa</a>
</div>
```

---

## 🔧 Konfigurácia

### Backend (Django)

**Email Backend (Development):**
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

**JWT Settings:**
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}
```

**Google OAuth (Optional):**
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

### Frontend (Angular)

**API URL:**
```typescript
// src/environments/environment.ts
export const environment = {
  apiUrl: 'http://localhost:8000/api'
};
```

---

## 🐳 Docker Setup

### Migrácie v Dockeri

```bash
# Build containers
docker-compose up --build

# Run migrations
docker-compose exec backend python manage.py makemigrations users
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser
```

---

## 🧪 Testing

### Backend Test (curl)

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'

# Get Profile (replace YOUR_ACCESS_TOKEN)
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Frontend Test Flow

1. **Registrácia:**
   - Choďte na http://localhost:4200/register
   - Vyplňte formulár
   - Kliknite "Registrovať sa"
   - Mali by ste byť automaticky prihlásený

2. **Prihlásenie:**
   - Choďte na http://localhost:4200/login
   - Zadajte email a heslo
   - Kliknite "Prihlásiť sa"

3. **Profil:**
   - Choďte na http://localhost:4200/profile
   - Zmeňte meno/priezvisko
   - Kliknite "Aktualizovať profil"
   - Zmeňte heslo (ak nie OAuth user)

4. **Odhlásenie:**
   - V profile kliknite "Odhlásiť sa"

---

## 🔒 Security Tips

### Development
- ✅ JWT token v localStorage je OK pre development
- ✅ Console email backend je OK

### Production
- ⚠️ Use httpOnly cookies pre refresh token
- ⚠️ Enable HTTPS
- ⚠️ Configure real SMTP email backend
- ⚠️ Use environment variables pre secrets
- ⚠️ Set DEBUG=False
- ⚠️ Configure ALLOWED_HOSTS
- ⚠️ Enable CORS properly

---

## 📚 Dokumentácia

- **AUTHENTICATION_README.md** - Kompletná dokumentácia
- **GOOGLE_OAUTH_SETUP.md** - Google OAuth setup guide
- **Backend code:** `django_calculators/users/`
- **Frontend code:** `frontend/src/app/` (services, guards, components)

---

## 🎯 Ďalšie kroky

1. ✅ **Základná autentifikácia implementovaná**
2. ⬜ **Google OAuth setup** (optional)
3. ⬜ **Email verification** (optional)
4. ⬜ **Password reset** (optional)
5. ⬜ **2FA** (optional)

---

## ❓ Troubleshooting

### "Cannot find module" errors
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

### "Migrations conflict"
```bash
python manage.py migrate --fake users zero
python manage.py migrate users
```

### "CORS error"
Check `CORS_ALLOWED_ORIGINS` in Django settings includes `http://localhost:4200`

### "Token not sent"
Check browser console and verify:
- authInterceptor is configured in app.config.ts
- Token exists in localStorage
- Request is going to correct API URL

---

## 💡 Príklady

### Ochrana route guards

```typescript
// app.routes.ts
{
  path: 'admin',
  component: AdminComponent,
  canActivate: [authGuard]  // Only authenticated users
}
```

### Custom permissions

```typescript
// admin.guard.ts
export const adminGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const user = authService.getCurrentUser();
  
  if (user?.is_staff) {
    return true;
  }
  
  router.navigate(['/']);
  return false;
};
```

### Password strength validator

```typescript
// validators.ts
export function passwordStrengthValidator(): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    const value = control.value;
    if (!value) return null;
    
    const hasNumber = /[0-9]/.test(value);
    const hasUpper = /[A-Z]/.test(value);
    const hasLower = /[a-z]/.test(value);
    const hasSpecial = /[!@#$%^&*]/.test(value);
    
    const valid = hasNumber && hasUpper && hasLower;
    return valid ? null : { passwordStrength: true };
  };
}
```

---

## 📞 Support

Pre otázky a problémy:
- Skontrolujte dokumentáciu v **AUTHENTICATION_README.md**
- Check console logs (browser & Django)
- Verify all dependencies installed
- Check migrations applied

**Happy coding! 🎉**
