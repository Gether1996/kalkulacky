import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { User } from '../../models/auth.models';

@Component({
  selector: 'app-user-profile',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  templateUrl: './user-profile.html',
  styleUrl: './user-profile.css',
})
export class UserProfile implements OnInit {
  user: User | null = null;
  profileForm: FormGroup;
  passwordForm: FormGroup;
  
  loading = false;
  profileMessage = '';
  profileError = '';
  
  passwordLoading = false;
  passwordMessage = '';
  passwordError = '';

  constructor(
    private fb: FormBuilder,
    private authService: AuthService
  ) {
    this.profileForm = this.fb.group({
      first_name: [''],
      last_name: [''],
      email_notifications: [true]
    });

    this.passwordForm = this.fb.group({
      old_password: ['', Validators.required],
      new_password: ['', [Validators.required, Validators.minLength(8)]],
      new_password_confirm: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    this.loadProfile();
  }

  loadProfile(): void {
    this.authService.getProfile().subscribe({
      next: (user) => {
        this.user = user;
        this.profileForm.patchValue({
          first_name: user.first_name || '',
          last_name: user.last_name || '',
          email_notifications: user.email_notifications !== false
        });
      },
      error: (error) => {
        console.error('Failed to load profile', error);
      }
    });
  }

  updateProfile(): void {
    if (this.profileForm.invalid) {
      return;
    }

    this.loading = true;
    this.profileMessage = '';
    this.profileError = '';

    this.authService.updateProfile(this.profileForm.value).subscribe({
      next: () => {
        this.loading = false;
        this.profileMessage = 'Profil bol úspešne aktualizovaný';
        setTimeout(() => this.profileMessage = '', 3000);
      },
      error: (error) => {
        this.loading = false;
        this.profileError = 'Nepodarilo sa aktualizovať profil';
      }
    });
  }

  changePassword(): void {
    if (this.passwordForm.invalid) {
      return;
    }

    const values = this.passwordForm.value;
    if (values.new_password !== values.new_password_confirm) {
      this.passwordError = 'Nové heslá sa nezhodujú';
      return;
    }

    this.passwordLoading = true;
    this.passwordMessage = '';
    this.passwordError = '';

    this.authService.changePassword(this.passwordForm.value).subscribe({
      next: () => {
        this.passwordLoading = false;
        this.passwordMessage = 'Heslo bolo úspešne zmenené';
        this.passwordForm.reset();
        setTimeout(() => this.passwordMessage = '', 3000);
      },
      error: (error) => {
        this.passwordLoading = false;
        this.passwordError = error.error?.old_password?.[0] || 'Nepodarilo sa zmeniť heslo';
      }
    });
  }

  logout(): void {
    this.authService.logout().subscribe();
  }

  confirmingDelete = false;
  deleting = false;

  deleteAccount(): void {
    this.deleting = true;
    this.authService.deleteAccount().subscribe({
      next: () => { this.deleting = false; },
      error: () => { this.deleting = false; this.confirmingDelete = false; },
    });
  }
}
