// Calculator Types
export interface CalculatorCard {
  id: string;
  title: string;
  description: string;
  icon: string;
  route: string;
  searchVolume: number;  // monthly searches
  color: string;
}

// Salary Calculator
export interface SalaryCalculationRequest {
  gross_salary: number;
  children_under_15?: number;  // Optional: children under 15 years (100 EUR/month each)
  children_15_to_18?: number;  // Optional: children 15-18 years (50 EUR/month each)
  apply_nontaxable_amount?: boolean;  // Optional: apply NČZD 497.23 EUR (default: true)
  has_disability?: boolean;  // Optional: ZŤP - reduces health insurance to 2.5% (default: false)
}

export interface SalaryCalculationResponse {
  gross_salary: number;
  social_insurance: number;
  health_insurance: number;
  tax_base: number;
  non_taxable_amount: number;
  taxable_base: number;
  income_tax: number;
  child_tax_bonus: number;
  children_under_15: number;
  children_15_to_18: number;
  total_children: number;
  apply_nontaxable_amount: boolean;
  has_disability: boolean;
  final_tax: number;
  net_salary: number;
  effective_tax_rate: number;
  super_gross_salary: number;
  total_employer_contributions: number;
}

// Mortgage Calculator
export interface MortgageCalculationRequest {
  loan_amount: number;
  annual_interest_rate: number;
  loan_term_years: number;
}

export interface MortgageCalculationResponse {
  loan_amount: number;
  annual_interest_rate: number;
  loan_term_years: number;
  monthly_payment: number;
  total_paid: number;  // Fixed: was total_payment
  total_interest: number;
  total_principal: number;
  first_year: FirstYearDetails;
  amortization_schedule: AmortizationEntry[];
  breakdown: MortgageBreakdown;
}

export interface FirstYearDetails {
  total_payment: number;
  principal: number;
  interest: number;
  remaining_balance: number;
}

export interface AmortizationEntry {
  year: number;  // Fixed: was month
  principal_paid: number;  // Fixed: was principal
  interest_paid: number;  // Fixed: was interest
  total_paid: number;  // Fixed: was payment
  remaining_balance: number;
}

export interface MortgageBreakdown {
  monthly_payment: number;
  number_of_payments: number;
  total_paid: number;
  loan_amount: number;
  total_interest: number;
  interest_percentage: number;
}

// VAT Calculator
export interface VATCalculationRequest {
  amount: number;
  vat_rate?: number;
  calculation_type: 'add_vat' | 'remove_vat';
}

export interface VATCalculationResponse {
  calculation_type: string;
  vat_rate: number;
  amount_without_vat: number;
  vat_amount: number;
  amount_with_vat: number;
  breakdown: VATBreakdown;
  slovak_vat_rates: SlovakVATRates;
}

export interface VATBreakdown {
  base_amount: number;
  vat_percentage: number;
  vat_amount: number;
  total_with_vat: number;
}

export interface SlovakVATRates {
  standard: number;
  reduced: number;
  zero: number;
}

// Blog Types

export interface BlogCategory {
  id: number;
  name: string;
  slug: string;
  description: string;
  color: string;
  icon: string;
  order: number;
  post_count: number;
  created_at: string;
}

export interface BlogPostSummary {
  id: number;
  title: string;
  slug: string;
  excerpt: string;
  featured_image_url?: string;
  category_name: string;
  category_slug: string;
  category_color: string;
  tags_list: string[];
  published_at: string;
  view_count: number;
  read_time: string;
  related_calculator?: string;
}

export interface BlogPostDetail {
  id: number;
  title: string;
  slug: string;
  excerpt: string;
  content_html: string;
  meta_keywords: string;
  featured_image_url?: string;
  category: BlogCategory;
  tags_list: string[];
  related_calculator?: string;
  status: string;
  published_at: string;
  view_count: number;
  read_time: string;
  related_posts: BlogPostSummary[];
  created_at: string;
  updated_at: string;
}
