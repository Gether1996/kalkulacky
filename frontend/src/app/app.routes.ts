import { Routes } from '@angular/router';
import { HomeComponent } from './components/home/home.component';

export const routes: Routes = [
  {
    path: '',
    component: HomeComponent
  },
  {
    path: 'calculator/salary',
    loadComponent: () => import('./components/salary-calculator/salary-calculator.component').then(m => m.SalaryCalculatorComponent)
  },
  {
    path: 'calculator/mortgage',
    loadComponent: () => import('./components/mortgage-calculator/mortgage-calculator.component').then(m => m.MortgageCalculatorComponent)
  },
  {
    path: 'calculator/vat',
    loadComponent: () => import('./components/vat-calculator/vat-calculator.component').then(m => m.VatCalculatorComponent)
  },
  {
    path: 'blog',
    loadComponent: () => import('./components/blog-list/blog-list.component').then(m => m.BlogListComponent)
  },
  {
    path: 'blog/:slug',
    loadComponent: () => import('./components/blog-detail/blog-detail.component').then(m => m.BlogDetailComponent)
  },
  {
    path: '**',
    redirectTo: ''
  }
];
