import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { User } from '../../models/auth.models';

@Component({
  selector: 'app-user-dashboard',
  imports: [CommonModule, RouterModule],
  templateUrl: './user-dashboard.html',
  styleUrl: './user-dashboard.css',
})
export class UserDashboard implements OnInit {
  currentUser: User | null = null;
  accountCreatedDate: Date | null = null;
  stats = {
    totalCalculations: 0,
    savedCalculations: 0,
    favoritesCount: 0
  };

  popularCalculators = [
    { name: 'Mzdová kalkulačka', route: '/calculator/salary', icon: '💰' },
    { name: 'Hypotekárna kalkulačka', route: '/calculator/mortgage', icon: '🏠' },
    { name: 'DPH kalkulačka', route: '/calculator/vat', icon: '🧾' },
    { name: 'BMI kalkulačka', route: '/calculator/bmi', icon: '⚖️' },
    { name: 'Tehotenská kalkulačka', route: '/calculator/pregnancy', icon: '👶' },
    { name: 'Dôchodková kalkulačka', route: '/calculator/pension', icon: '👴' }
  ];

  constructor(private authService: AuthService) {}

  ngOnInit() {
    // Subscribe to current user observable
    this.authService.currentUser$.subscribe(user => {
      this.currentUser = user;
      if (this.currentUser) {
        this.loadUserData();
      }
    });
  }

  loadUserData() {
    // Simulate loading user data - in real app, this would be an API call
    this.accountCreatedDate = new Date(); // Replace with actual date from backend
    this.stats = {
      totalCalculations: 0,
      savedCalculations: 0,
      favoritesCount: 0
    };
  }

  getUserInitials(): string {
    if (!this.currentUser) return '';
    
    if (this.currentUser.first_name && this.currentUser.last_name) {
      return `${this.currentUser.first_name[0]}${this.currentUser.last_name[0]}`.toUpperCase();
    }
    
    if (this.currentUser.first_name) {
      return this.currentUser.first_name.substring(0, 2).toUpperCase();
    }
    
    if (this.currentUser.email) {
      return this.currentUser.email.substring(0, 2).toUpperCase();
    }
    
    return 'U';
  }

  getUserDisplayName(): string {
    if (!this.currentUser) return '';
    
    if (this.currentUser.first_name && this.currentUser.last_name) {
      return `${this.currentUser.first_name} ${this.currentUser.last_name}`;
    }
    
    if (this.currentUser.first_name) {
      return this.currentUser.first_name;
    }
    
    return this.currentUser.email;
  }

  formatDate(date: Date | null): string {
    if (!date) return 'N/A';
    return new Intl.DateTimeFormat('sk-SK', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    }).format(date);
  }
}
