import { Routes } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { authGuard, guestGuard } from './guards/auth.guard';

export const routes: Routes = [
  {
    path: '',
    component: HomeComponent
  },
  {
    path: 'calculator/basic',
    loadComponent: () => import('./components/basic-calculator/basic-calculator.component').then(m => m.BasicCalculatorComponent)
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
    path: 'calculator/loan',
    loadComponent: () => import('./components/loan-calculator/loan-calculator.component').then(m => m.LoanCalculatorComponent)
  },
  {
    path: 'calculator/fuel-cost',
    loadComponent: () => import('./components/fuel-cost-calculator/fuel-cost-calculator.component').then(m => m.FuelCostCalculatorComponent)
  },
  {
    path: 'calculator/bmi',
    loadComponent: () => import('./components/bmi-calculator/bmi-calculator.component').then(m => m.BmiCalculatorComponent)
  },
  {
    path: 'calculator/percentage',
    loadComponent: () => import('./components/percentage-calculator/percentage-calculator.component').then(m => m.PercentageCalculatorComponent)
  },
  {
    path: 'calculator/pregnancy',
    loadComponent: () => import('./components/pregnancy-calculator/pregnancy-calculator.component').then(m => m.PregnancyCalculatorComponent)
  },
  {
    path: 'calculator/pension',
    loadComponent: () => import('./components/pension-calculator/pension-calculator.component').then(m => m.PensionCalculatorComponent)
  },
  {
    path: 'calculator/vacation',
    loadComponent: () => import('./components/vacation-calculator/vacation-calculator.component').then(m => m.VacationCalculatorComponent)
  },
  {
    path: 'calculator/energy',
    loadComponent: () => import('./components/energy-calculator/energy-calculator.component').then(m => m.EnergyCalculatorComponent)
  },
  {
    path: 'calculator/bmr',
    loadComponent: () => import('./components/bmr-calculator/bmr-calculator.component').then(m => m.BmrCalculatorComponent)
  },
  {
    path: 'calculator/payment',
    loadComponent: () => import('./components/payment-calculator/payment-calculator.component').then(m => m.PaymentCalculatorComponent)
  },
  {
    path: 'calculator/freelancer-tax',
    loadComponent: () => import('./components/freelancer-tax-calculator/freelancer-tax-calculator.component').then(m => m.FreelancerTaxCalculatorComponent)
  },
  {
    path: 'calculator/inflation',
    loadComponent: () => import('./components/inflation-calculator/inflation-calculator.component').then(m => m.InflationCalculatorComponent)
  },
  {
    path: 'calculator/roi',
    loadComponent: () => import('./components/roi-calculator/roi-calculator.component').then(m => m.RoiCalculatorComponent)
  },
  {
    path: 'calculator/hours-worked',
    loadComponent: () => import('./components/hours-worked-calculator/hours-worked-calculator.component').then(m => m.HoursWorkedCalculatorComponent)
  },
  {
    path: 'calculator/unit-converter',
    loadComponent: () => import('./components/unit-converter/unit-converter.component').then(m => m.UnitConverterComponent)
  },
  {
    path: 'calculator/sick-leave',
    loadComponent: () => import('./components/sick-leave-calculator/sick-leave-calculator.component').then(m => m.SickLeaveCalculatorComponent)
  },
  {
    path: 'calculator/car-leasing',
    loadComponent: () => import('./components/car-leasing-calculator/car-leasing-calculator.component').then(m => m.CarLeasingCalculatorComponent)
  },
  {
    path: 'calculator/area-volume',
    loadComponent: () => import('./components/area-volume-calculator/area-volume-calculator.component').then(m => m.AreaVolumeCalculatorComponent)
  },
  {
    path: 'calculator/split-bill',
    loadComponent: () => import('./components/split-bill-calculator/split-bill-calculator.component').then(m => m.SplitBillCalculatorComponent)
  },
  {
    path: 'calculator/parental-benefit',
    loadComponent: () => import('./components/parental-benefit-calculator/parental-benefit-calculator.component').then(m => m.ParentalBenefitCalculatorComponent)
  },
  {
    path: 'calculator/solar',
    loadComponent: () => import('./components/solar-calculator/solar-calculator.component').then(m => m.SolarCalculatorComponent)
  },
  {
    path: 'calculator/heat-pump',
    loadComponent: () => import('./components/heat-pump-calculator/heat-pump-calculator.component').then(m => m.HeatPumpCalculatorComponent)
  },
  {
    path: 'calculator/renovation',
    loadComponent: () => import('./components/renovation-grant-calculator/renovation-grant-calculator.component').then(m => m.RenovationGrantCalculatorComponent)
  },
  {
    path: 'calculator/car-insurance',
    loadComponent: () => import('./components/car-insurance-calculator/car-insurance-calculator.component').then(m => m.CarInsuranceCalculatorComponent)
  },
  {
    path: 'energia',
    loadComponent: () => import('./components/energy-hub/energy-hub.component').then(m => m.EnergyHubComponent)
  },
  {
    path: 'cista-mzda/:amount',
    loadComponent: () => import('./components/salary-value-page/salary-value-page.component').then(m => m.SalaryValuePageComponent)
  },
  {
    path: 'embed/:type',
    loadComponent: () => import('./components/embed/embed.component').then(m => m.EmbedComponent)
  },
  {
    path: 'privacy',
    loadComponent: () => import('./components/legal/privacy-policy.component').then(m => m.PrivacyPolicyComponent)
  },
  {
    path: 'terms',
    loadComponent: () => import('./components/legal/terms.component').then(m => m.TermsComponent)
  },
  {
    path: 'cookies',
    loadComponent: () => import('./components/legal/cookies.component').then(m => m.CookiesComponent)
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
    path: 'login',
    loadComponent: () => import('./components/login/login').then(m => m.Login),
    canActivate: [guestGuard]
  },
  {
    path: 'register',
    loadComponent: () => import('./components/register/register').then(m => m.Register),
    canActivate: [guestGuard]
  },
  {
    path: 'forgot-password',
    loadComponent: () => import('./components/forgot-password/forgot-password.component').then(m => m.ForgotPasswordComponent),
    canActivate: [guestGuard]
  },
  {
    path: 'reset-password',
    loadComponent: () => import('./components/reset-password/reset-password.component').then(m => m.ResetPasswordComponent)
  },
  {
    path: 'dashboard',
    loadComponent: () => import('./components/user-dashboard/user-dashboard').then(m => m.UserDashboard),
    canActivate: [authGuard]
  },
  {
    path: 'profile',
    loadComponent: () => import('./components/user-profile/user-profile').then(m => m.UserProfile),
    canActivate: [authGuard]
  },
  {
    path: '**',
    loadComponent: () => import('./components/not-found/not-found.component').then(m => m.NotFoundComponent)
  }
];
