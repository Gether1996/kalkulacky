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

// Loan Calculator
export interface LoanCalculationRequest {
  loan_amount: number;
  interest_rate: number;
  loan_years: number;
  include_schedule?: boolean;
}

export interface LoanCalculationResponse {
  monthly_payment: number;
  total_interest: number;
  total_paid: number;
  principal: number;
  annual_interest_rate: number;
  loan_years: number;
  total_months: number;
  monthly_interest_rate: number;
  amortization_schedule?: LoanAmortizationEntry[];
  schedule_summary?: LoanScheduleSummary;
}

export interface LoanAmortizationEntry {
  month: number;
  payment: number;
  principal_payment: number;
  interest_payment: number;
  remaining_balance: number;
}

export interface LoanScheduleSummary {
  first_year_interest: number;
  first_year_principal: number;
}

// Fuel Cost Calculator
export interface FuelCostCalculationRequest {
  distance: number;
  consumption: number;
  fuel_price: number;
}

export interface FuelCostCalculationResponse {
  distance: number;
  consumption: number;
  fuel_price: number;
  fuel_needed: number;
  total_cost: number;
  cost_per_km: number;
  return_trip: {
    distance: number;
    fuel_needed: number;
    total_cost: number;
  };
}

// BMI Calculator
export interface BMICalculationRequest {
  weight: number;
  height: number;
}

export interface BMICalculationResponse {
  bmi: number;
  weight: number;
  height: number;
  height_meters: number;
  category: string;
  category_sk: string;
  category_description: string;
  health_risk: string;
  ideal_weight_range: {
    min: number;
    max: number;
  };
  weight_to_change: number;
  recommendation: string;
  is_healthy: boolean;
}

// Percentage/Math Calculator
export interface PercentageCalculationRequest {
  calculation_type: string;
  value1?: number;
  value2?: number;
  percent?: number;
}

export interface PercentageCalculationResponse {
  calculation_type: string;
  input_values: any;
  result: number;
  formula?: string;
  absolute_change?: number;
  percent_change?: number;
  is_increase?: boolean;
  increase_amount?: number;
  decrease_amount?: number;
}

// Pregnancy Calculator
export interface PregnancyCalculationRequest {
  calculation_method: 'lmp' | 'conception';
  lmp_date?: string;
  conception_date?: string;
  current_date?: string;
}

export interface PregnancyCalculationResponse {
  due_date: string;
  lmp_date: string;
  conception_date: string;
  current_week: number;
  current_day: number;
  total_days_pregnant: number;
  days_remaining: number;
  trimester: number;
  trimester_progress: number;
  pregnancy_progress: number;
  is_past_due: boolean;
  weeks_description: string;
  calculation_method: string;
}

// Pension Calculator
export interface PensionCalculationRequest {
  current_age: number;
  gross_salary: number;
  years_worked: number;
  gender?: 'male' | 'female';
  include_second_pillar?: boolean;
  second_pillar_rate?: number;
}

export interface PensionContributions {
  employee_monthly: number;
  employer_monthly: number;
  total_monthly: number;
  first_pillar_monthly: number;
  second_pillar_monthly: number;
  total_contributed_so_far: number;
  total_future_contributions: number;
  total_lifetime_contributions: number;
}

export interface PensionSystem {
  include_second_pillar: boolean;
  first_pillar_rate: number;
  second_pillar_rate: number;
  minimum_pension: number;
}

export interface PensionProjections {
  life_expectancy_after_retirement: number;
  total_pension_lifetime: number;
  roi_percentage: number;
}

export interface PensionCalculationResponse {
  current_age: number;
  retirement_age: number;
  years_to_retirement: number;
  already_retired: boolean;
  years_worked: number;
  total_years_at_retirement: number;
  gross_salary: number;
  estimated_monthly_pension: number;
  replacement_rate: number;
  contributions: PensionContributions;
  pension_system: PensionSystem;
  projections: PensionProjections;
}

// Vacation Days Calculator
export interface VacationCalculationRequest {
  age: number;
  employment_start_date: string;
  current_date?: string;
  vacation_days_used?: number;
  days_carried_over?: number;
  planned_vacation_days?: number;
}

export interface VacationEntitlement {
  annual_entitlement: number;
  base_days: number;
  age_bonus: number;
  has_age_bonus: boolean;
  age_threshold: number;
}

export interface VacationCurrentYear {
  days_accrued: number;
  days_carried_over: number;
  total_available: number;
  days_used: number;
  remaining_days: number;
  weeks_available: number;
  weeks_used: number;
}

export interface VacationPlanning {
  planned_vacation_days: number;
  days_after_planned: number;
  can_take_planned: boolean;
}

export interface VacationAccrual {
  accrual_per_month: number;
  months_until_year_end: number;
  projected_accrual_by_year_end: number;
}

export interface VacationStatus {
  is_over_limit: boolean;
  usage_percentage: number;
}

export interface VacationCalculationResponse {
  age: number;
  employment_start_date: string;
  is_first_year: boolean;
  entitlement: VacationEntitlement;
  current_year: VacationCurrentYear;
  planning: VacationPlanning;
  accrual: VacationAccrual;
  status: VacationStatus;
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

// Energy Cost Calculator

export interface EnergyCalculationRequest {
  electricity_consumption: number;
  gas_consumption?: number;
  electricity_rate?: number;
  gas_rate?: number;
  has_dual_tariff?: boolean;
  high_tariff_percentage?: number;
  household_size?: number;
}

export interface EnergyCalculationResponse {
  electricity: ElectricityDetails;
  gas: GasDetails;
  total: TotalEnergyCost;
  household: HouseholdDetails;
  averages: EnergyAverages;
}

export interface ElectricityDetails {
  consumption_kwh: number;
  rate: number;
  has_dual_tariff: boolean;
  high_tariff_kwh: number | null;
  low_tariff_kwh: number | null;
  variable_cost: number;
  fixed_cost: number;
  total_monthly: number;
  total_annual: number;
  vs_average_percentage: number;
}

export interface GasDetails {
  consumption_kwh: number;
  rate: number;
  variable_cost: number;
  fixed_cost: number;
  total_monthly: number;
  total_annual: number;
  vs_average_percentage: number | null;
}

export interface TotalEnergyCost {
  monthly_cost: number;
  annual_cost: number;
  electricity_percentage: number;
  gas_percentage: number;
}

export interface HouseholdDetails {
  household_size: number;
  cost_per_person_monthly: number;
  cost_per_person_annual: number;
  electricity_per_person: number;
  efficiency_category: string;
}

export interface EnergyAverages {
  avg_electricity_monthly_kwh: number;
  avg_gas_monthly_kwh: number;
  avg_electricity_cost: number;
  avg_gas_cost: number | null;
}

// BMR Calculator

export interface BMRCalculationRequest {
  weight: number;
  height: number;
  age: number;
  gender: 'male' | 'female';
  activity_level?: 'sedentary' | 'light' | 'moderate' | 'active' | 'very_active';
  weight_goal?: 'lose_fast' | 'lose_moderate' | 'lose_slow' | 'maintain' | 'gain_slow' | 'gain_moderate' | 'gain_fast';
}

export interface BMRCalculationResponse {
  bmr: BMRValues;
  tdee: TDEEValues;
  recommendations: CalorieRecommendations;
  macros: MacronutrientBreakdown;
  profile: UserProfile;
}

export interface BMRValues {
  mifflin_st_jeor: number;
  harris_benedict: number;
  recommended: number;
}

export interface TDEEValues {
  calories: number;
  activity_level: string;
  activity_description: string;
  activity_multiplier: number;
}

export interface CalorieRecommendations {
  weight_goal: string;
  goal_description: string;
  calorie_adjustment: number;
  target_calories: number;
  is_below_minimum: boolean;
  min_safe_calories: number;
  kg_per_week: number | null;
}

export interface MacronutrientBreakdown {
  protein: MacroDetail;
  carbs: MacroDetail;
  fats: MacroDetail;
}

export interface MacroDetail {
  grams: number;
  calories: number;
  percentage: number;
}

export interface UserProfile {
  weight: number;
  height: number;
  age: number;
  gender: string;
  bmi: number;
}

// Payment Calculator

export interface PaymentCalculationRequest {
  loan_amount: number;
  annual_interest_rate: number;
  loan_term_years: number;
  payment_frequency?: 'monthly' | 'quarterly' | 'yearly';
  include_schedule?: boolean;
}

export interface PaymentCalculationResponse {
  payment: PaymentDetails;
  loan: LoanDetails;
  totals: PaymentTotals;
  breakdown: PaymentBreakdown;
  schedule?: AmortizationScheduleItem[];
}

export interface PaymentDetails {
  amount: number;
  frequency: string;
  frequency_label: string;
  payments_per_year: number;
  total_payments: number;
  yearly_amount: number;
}

export interface LoanDetails {
  principal: number;
  interest_rate: number;
  term_years: number;
  period_interest_rate: number;
}

export interface PaymentTotals {
  total_paid: number;
  total_interest: number;
  interest_percentage: number;
  principal_percentage: number;
}

export interface PaymentBreakdown {
  first_payment: {
    payment: number;
    principal: number;
    interest: number;
  };
}

export interface AmortizationScheduleItem {
  payment_number: number;
  payment: number;
  principal: number;
  interest: number;
  remaining_balance: number;
}

// Freelancer Tax Calculator Types

export interface FreelancerTaxCalculationRequest {
  annual_revenue: number;
  annual_expenses?: number;
  use_flat_expenses?: boolean;
  include_sickness?: boolean;
  months_active?: number;
}

export interface FreelancerTaxCalculationResponse {
  income: IncomeDetails;
  tax: TaxDetails;
  health_insurance: HealthInsuranceDetails;
  social_insurance: SocialInsuranceDetails;
  summary: TaxSummary;
}

export interface IncomeDetails {
  annual_revenue: number;
  annual_expenses: number;
  expenses_note: string;
  tax_base: number;
  non_taxable_amount: number;
  taxable_income: number;
}

export interface TaxDetails {
  income_tax: number;
  tax_rate_applied: number;
  monthly_average: number;
}

export interface HealthInsuranceDetails {
  monthly_base: number;
  monthly_payment: number;
  annual_payment: number;
  rate: number;
  min_base: number;
}

export interface SocialInsuranceDetails {
  monthly_base: number;
  monthly_payment: number;
  annual_payment: number;
  breakdown: SocialInsuranceBreakdown;
}

export interface SocialInsuranceBreakdown {
  sickness: ContributionDetail;
  pension: ContributionDetail;
  disability: ContributionDetail;
  accident: ContributionDetail;
  guarantee: ContributionDetail;
  reserve: ContributionDetail;
}

export interface ContributionDetail {
  monthly: number;
  annual: number;
  rate: number;
  included?: boolean;
}

export interface TaxSummary {
  total_contributions: number;
  total_tax_and_contributions: number;
  net_income: number;
  effective_rate: number;
  monthly_revenue: number;
  monthly_deductions: number;
  monthly_net: number;
  months_active: number;
}

// Inflation Calculator Types

export interface InflationCalculationRequest {
  present_value: number;
  years: number;
  inflation_rate?: number;
  calculate_reverse?: boolean;
}

export interface InflationCalculationResponse {
  input: InflationInput;
  result: InflationResult;
  analysis: InflationAnalysis;
  yearly_breakdown: YearlyBreakdownItem[];
  comparison: InflationComparison[];
}

export interface InflationInput {
  present_value: number;
  years: number;
  inflation_rate: number;
  calculation_type: string;
}

export interface InflationResult {
  future_value: number;
  total_inflation: number;
  total_inflation_percent: number;
  purchasing_power: number;
  required_future_value: number;
  cumulative_inflation_rate: number;
  avg_annual_change: number;
}

export interface InflationAnalysis {
  power_category: string;
  power_description: string;
  yearly_loss: number;
  effective_rate: number;
}

export interface YearlyBreakdownItem {
  year: number;
  value: number;
  change: number;
  cumulative_inflation: number;
  purchasing_power: number;
}

export interface InflationComparison {
  inflation_rate: number;
  value: number;
  difference: number;
  difference_percent: number;
}

// ROI Calculator Types

export interface ROICalculationRequest {
  initial_investment: number;
  final_value: number;
  additional_costs?: number;
  investment_period_months?: number | null;
}

export interface ROICalculationResponse {
  investment: InvestmentDetails;
  returns: ReturnsDetails;
  performance: PerformanceDetails;
  analysis: AnalysisDetails;
}

export interface InvestmentDetails {
  initial_investment: number;
  additional_costs: number;
  total_investment: number;
  final_value: number;
}

export interface ReturnsDetails {
  net_profit: number;
  roi_percentage: number;
  margin: number;
  markup: number;
  status: string;
  status_description: string;
}

export interface PerformanceDetails {
  category: string;
  description: string;
  investment_period_months: number | null;
  investment_years: number | null;
  annualized_roi: number | null;
  payback_period_months: number | null;
  payback_period_years: number | null;
}

export interface AnalysisDetails {
  return_multiple: number;
  profit_per_invested: number;
  comparisons: BenchmarkComparison[];
}

export interface BenchmarkComparison {
  benchmark: string;
  benchmark_roi: number;
  difference: number;
  better: boolean;
}

// Hours Worked Calculator
export interface HoursWorkedCalculationRequest {
  hours_worked: number;
  hourly_rate?: number | null;
  period_type?: string;
  weekend_hours?: number;
  holiday_hours?: number;
}

export interface HoursWorkedCalculationResponse {
  hours: HoursDetails;
  percentages: PercentagesDetails;
  earnings?: EarningsDetails;
  analysis: HoursAnalysisDetails;
  rates: RatesDetails;
}

export interface HoursDetails {
  total_hours: number;
  standard_hours: number;
  regular_hours: number;
  overtime_hours: number;
  overtime_breakdown: OvertimeBreakdown;
}

export interface OvertimeBreakdown {
  regular_overtime: number;
  weekend_overtime: number;
  holiday_overtime: number;
}

export interface PercentagesDetails {
  regular_percentage: number;
  overtime_percentage: number;
}

export interface EarningsDetails {
  regular_earnings: number;
  overtime_earnings: number;
  overtime_breakdown: OvertimeBreakdown;
  total_earnings: number;
  average_hourly_effective: number;
}

export interface HoursAnalysisDetails {
  period_type: string;
  balance_category: string;
  balance_description: string;
  daily_average: number | null;
  exceeds_standard: boolean;
  excess_hours: number;
}

export interface RatesDetails {
  hourly_rate?: number;
  multipliers: MultipliersInfo;
}

export interface MultipliersInfo {
  basic: number;
  weekend: number;
  holiday: number;
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

// Unit Converter
export interface UnitConverterRequest {
  value: number;
  from_unit: string;
  to_unit: string;
  category: string;
}

export interface UnitConverterResponse {
  value: number;
  from_unit: string;
  from_unit_name: string;
  to_unit: string;
  to_unit_name: string;
  result: number;
  category: string;
  category_name: string;
  formula: string;
}

export interface UnitCategory {
  value: string;
  label: string;
}

export interface UnitOption {
  value: string;
  label: string;
}

// Sick Leave Calculator (Nemocenská)
export interface SickLeaveCalculationRequest {
  gross_salary: number;
  days_sick: number;
  leave_type: 'illness' | 'care';
}

export interface SickLeaveCalculationResponse {
  gross_salary: number;
  days_sick: number;
  leave_type: string;
  leave_type_label: string;
  yearly_salary: number;
  daily_assessment_base: number;
  capped_daily_base: number;
  is_capped: boolean;
  max_daily_base: number;
  employer_payment_days: number;
  insurance_payment_days: number;
  employer_rate_percent: number;
  insurance_rate_percent: number;
  employer_payment: number;
  insurance_payment: number;
  total_sick_leave: number;
  avg_daily_rate: number;
  full_salary_for_period: number;
  loss_vs_full_salary: number;
  loss_percentage: number;
  explanation: string;
  breakdown: SickLeaveDayBreakdown[];
}

export interface SickLeaveDayBreakdown {
  day: number;
  payer: string;
  rate_percent: number;
  daily_amount: number;
}

// Car Leasing Calculator
export interface CarLeasingCalculationRequest {
  car_price: number;
  down_payment: number;
  term_months: number;
  leasing_rate: number;
  loan_rate: number;
  residual_value_percent: number;
  include_vat: boolean;
}

export interface CarLeasingOption {
  option_type: string;
  option_name: string;
  initial_cost: number;
  monthly_payment: number;
  final_payment: number;
  total_cost: number;
  ownership: string;
  explanation: string;
}

export interface CarLeasingCalculationResponse {
  car_price: number;
  down_payment: number;
  term_months: number;
  include_vat: boolean;
  options: {
    financial_leasing: CarLeasingOption;
    operational_leasing: CarLeasingOption;
    loan: CarLeasingOption;
    cash: CarLeasingOption;
  };
  comparison: {
    cheapest: string;
    most_expensive: string;
    cheapest_monthly: string;
    ownership_options: string[];
  };
}

// Area & Volume Calculator
export interface AreaVolumeCalculationRequest {
  shape: string;
  dimensions: { [key: string]: number };
}

export interface AreaVolumeCalculationResponse {
  shape: string;
  shape_name: string;
  type: string;
  result: number;
  result_label: string;
  secondary_result?: number;
  secondary_label?: string;
  formula: string;
  dimensions: { [key: string]: number };
  unit: string;
}

export interface ShapeInfo {
  id: string;
  name: string;
  type: string;
  icon: string;
  dimensions: string[];
  dimension_labels: { [key: string]: string };
}

export interface AvailableShapes {
  '2d': ShapeInfo[];
  '3d': ShapeInfo[];
}

// Split Bill Calculator
export interface SplitBillCalculationRequest {
  split_type: 'equal' | 'by_items' | 'custom';
  total_amount?: number;
  num_people?: number;
  tip_percent?: number;
  items?: BillItem[];
  custom_amounts?: CustomAmount[];
}

export interface BillItem {
  person: string;
  amount: number;
}

export interface CustomAmount {
  person: string;
  amount: number;
}

export interface PersonBreakdown {
  person: string;
  subtotal: number;
  tip: number;
  total: number;
}

export interface SplitBillCalculationResponse {
  split_type: string;
  original_amount: number;
  tip_percent: number;
  tip_amount: number;
  total_with_tip: number;
  num_people: number;
  breakdown: PersonBreakdown[];
  per_person_average?: number;
}

export interface TipSuggestion {
  id: string;
  label: string;
  percent: number;
  tip_amount: number;
  total: number;
}

export interface TipSuggestionsResponse {
  amount: number;
  suggestions: TipSuggestion[];
}

