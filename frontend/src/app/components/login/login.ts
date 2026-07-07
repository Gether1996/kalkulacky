import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterModule, ActivatedRoute } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { PasswordInputComponent } from '../shared/password-input/password-input.component';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule, PasswordInputComponent],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login implements OnInit {
  loginForm: FormGroup;
  loading = false;
  errorMessage = '';
  returnUrl = '/';

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]]
    });

    // Accept both param names: the auth guard uses `returnUrl`, while the
    // login-gated widgets (save-calculation, rating, savings-goal, home) use
    // `redirect`. Honour whichever is present so users always land back.
    const q = this.route.snapshot.queryParams;
    this.returnUrl = q['returnUrl'] || q['redirect'] || '/';
  }

  ngOnInit() {
    this.loadGoogleScript();
  }

  private loadGoogleScript() {
    // @ts-ignore
    if (typeof google !== 'undefined' && google.accounts) {
      // @ts-ignore
      google.accounts.id.initialize({
        client_id: '456484596206-qqanoqeeiqr577vkn5pqs3d83nbiqhgt.apps.googleusercontent.com',
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
  }

  private handleGoogleResponse(response: any) {
    const idToken = response.credential;
    this.loading = true;
    this.errorMessage = '';
    
    this.authService.googleAuth(idToken).subscribe({
      next: () => {
        this.router.navigate([this.returnUrl]);
      },
      error: (error) => {
        this.loading = false;
        this.errorMessage = 'Google prihlásenie zlyhalo';
        console.error('Google auth error:', error);
      }
    });
  }

  onSubmit(): void {
    if (this.loginForm.invalid) {
      return;
    }

    this.loading = true;
    this.errorMessage = '';

    this.authService.login(this.loginForm.value).subscribe({
      next: () => {
        this.router.navigate([this.returnUrl]);
      },
      error: (error) => {
        this.loading = false;
        this.errorMessage = error.error?.detail || error.error?.non_field_errors?.[0] || 'Login failed. Please check your credentials.';
      }
    });
  }

  loginWithGoogle(): void {
    // Google One Tap prompt (alternative to button)
    // @ts-ignore
    google.accounts.id.prompt((notification: any) => {
      if (notification.isNotDisplayed()) {
        console.log('Google One Tap not displayed');
      } else if (notification.isSkippedMoment()) {
        console.log('Google One Tap skipped');
      }
    });
  }

  get email() {
    return this.loginForm.get('email');
  }

  get password() {
    return this.loginForm.get('password');
  }
}
