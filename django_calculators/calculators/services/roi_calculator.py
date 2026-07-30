"""
ROI (Return on Investment) Calculator Service
Calculate return on investment, profit margins, and investment performance metrics.
"""
from decimal import Decimal
from typing import Dict, Any
from .base_calculator import BaseCalculator


class ROICalculator(BaseCalculator):
    """
    Calculate Return on Investment (ROI) and related metrics.
    
    Includes:
    - ROI percentage
    - Net profit/loss
    - Annualized ROI
    - Payback period
    - Investment performance analysis
    """
    
    def calculate(
        self,
        initial_investment: float,
        final_value: float,
        additional_costs: float = 0,
        investment_period_months: int = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Calculate ROI and investment performance metrics.
        
        Parameters:
        - initial_investment: Initial amount invested
        - final_value: Final value of investment (or current value)
        - additional_costs: Additional costs incurred (optional, default 0)
        - investment_period_months: Duration of investment in months (optional, for annualized ROI)
        
        Returns:
        Dictionary with ROI calculations
        """
        initial_investment = Decimal(str(initial_investment))
        final_value = Decimal(str(final_value))
        additional_costs = Decimal(str(additional_costs))
        investment_period_months = investment_period_months
        
        # Validate inputs
        if initial_investment <= 0:
            raise ValueError("Počiatočná investícia musí byť kladná")
        
        if final_value < 0:
            raise ValueError("Konečná hodnota nesmie byť záporná")
        
        if additional_costs < 0:
            raise ValueError("Dodatočné náklady nesmú byť záporné")
        
        if investment_period_months is not None:
            investment_period_months = int(investment_period_months)
            if investment_period_months < 1:
                raise ValueError("Obdobie investície musí byť aspoň 1 mesiac")
            if investment_period_months > 1200:  # 100 years
                raise ValueError("Obdobie investície nemôže presiahnuť 1200 mesiacov (100 rokov)")
        
        # Calculate total investment (initial + additional costs)
        total_investment = initial_investment + additional_costs
        
        # Calculate net profit/loss
        net_profit = final_value - total_investment
        
        # Calculate ROI percentage
        # ROI = (Final Value - Total Investment) / Total Investment × 100
        roi_percentage = (net_profit / total_investment) * Decimal('100')
        
        # Determine profit/loss status
        if net_profit > 0:
            status = "Zisk"
            status_description = "Investícia je zisková"
        elif net_profit < 0:
            status = "Strata"
            status_description = "Investícia je stratová"
        else:
            status = "Neutrálna"
            status_description = "Bez zisku ani straty"
        
        # Calculate margin
        # Margin = Net Profit / Final Value × 100
        margin = (net_profit / final_value * Decimal('100')) if final_value > 0 else Decimal('0')
        
        # Calculate markup
        # Markup = Net Profit / Total Investment × 100 (same as ROI)
        markup = roi_percentage
        
        # Annualized ROI (if investment period is provided)
        annualized_roi = None
        investment_years = None
        if investment_period_months is not None and investment_period_months > 0:
            investment_years = Decimal(str(investment_period_months)) / Decimal('12')

            # True annualized return (CAGR): ((final / initial)^(1/years) - 1) × 100.
            # The n-th root is irrational, so the fractional power is done in float
            # (a rate, not a monetary amount) and converted back to Decimal; display
            # is rounded to 2 dp by round_decimal below.
            if investment_years > 0:
                total_return_multiplier = Decimal('1') + (roi_percentage / Decimal('100'))
                if total_return_multiplier > 0:
                    mult = float(total_return_multiplier)
                    cagr = (mult ** (1.0 / float(investment_years)) - 1.0) * 100.0
                    annualized_roi = Decimal(str(cagr))
                else:
                    # Total loss (or worse) — CAGR is undefined; fall back to linear.
                    annualized_roi = roi_percentage / investment_years
        
        # Payback period (months)
        # If positive ROI, calculate how long to recover initial investment
        payback_period_months = None
        payback_period_years = None
        
        if investment_period_months is not None and net_profit > 0 and investment_period_months > 0:
            # Simple payback: (Initial Investment / (Final Value / Period)) 
            # = Initial Investment × Period / Final Value
            monthly_return = final_value / Decimal(str(investment_period_months))
            if monthly_return > 0:
                payback_period_months = total_investment / monthly_return
                payback_period_years = payback_period_months / Decimal('12')
        
        # Performance category
        if roi_percentage >= 100:
            performance_category = "Výborná"
            performance_description = "Investícia priniesla viac ako dvojnásobok"
        elif roi_percentage >= 50:
            performance_category = "Veľmi dobrá"
            performance_description = "Vysoká návratnosť investície"
        elif roi_percentage >= 20:
            performance_category = "Dobrá"
            performance_description = "Solídna návratnosť investície"
        elif roi_percentage >= 10:
            performance_category = "Priemerná"
            performance_description = "Priemernávratnosť investície"
        elif roi_percentage >= 0:
            performance_category = "Slabá"
            performance_description = "Nízka návratnosť investície"
        elif roi_percentage >= -20:
            performance_category = "Strata"
            performance_description = "Menšia strata na investícii"
        elif roi_percentage >= -50:
            performance_category = "Veľká strata"
            performance_description = "Výrazná strata na investícii"
        else:
            performance_category = "Kritická strata"
            performance_description = "Veľmi vysoká strata na investícii"
        
        # Comparison with common benchmarks
        benchmarks = [
            {"name": "Úspory v banke", "roi": Decimal('2')},
            {"name": "Štátne dlhopisy", "roi": Decimal('3')},
            {"name": "Indexové fondy", "roi": Decimal('8')},
            {"name": "Akciový trh (priemer)", "roi": Decimal('10')},
            {"name": "Vysoko rizikové investície", "roi": Decimal('20')}
        ]
        
        comparisons = []
        for benchmark in benchmarks:
            if annualized_roi is not None:
                # Compare with annualized ROI
                diff = annualized_roi - benchmark["roi"]
            else:
                # Compare with total ROI
                diff = roi_percentage - benchmark["roi"]
            
            comparisons.append({
                "benchmark": benchmark["name"],
                "benchmark_roi": float(benchmark["roi"]),
                "difference": self.round_decimal(diff, 2),
                "better": diff > 0
            })
        
        result = {
            'investment': {
                'initial_investment': self.round_decimal(initial_investment),
                'additional_costs': self.round_decimal(additional_costs),
                'total_investment': self.round_decimal(total_investment),
                'final_value': self.round_decimal(final_value)
            },
            'returns': {
                'net_profit': self.round_decimal(net_profit),
                'roi_percentage': self.round_decimal(roi_percentage, 2),
                'margin': self.round_decimal(margin, 2),
                'markup': self.round_decimal(markup, 2),
                'status': status,
                'status_description': status_description
            },
            'performance': {
                'category': performance_category,
                'description': performance_description,
                'investment_period_months': investment_period_months,
                'investment_years': self.round_decimal(investment_years, 2) if investment_years else None,
                'annualized_roi': self.round_decimal(annualized_roi, 2) if annualized_roi is not None else None,
                'payback_period_months': self.round_decimal(payback_period_months, 1) if payback_period_months else None,
                'payback_period_years': self.round_decimal(payback_period_years, 2) if payback_period_years else None
            },
            'analysis': {
                'return_multiple': self.round_decimal(final_value / total_investment, 2),
                'profit_per_invested': self.round_decimal(net_profit / total_investment, 2),
                'comparisons': comparisons
            }
        }
        
        return result
    
    def get_metadata(self) -> Dict[str, Any]:
        """Return metadata about the ROI calculator."""
        return {
            'name': 'ROI Calculator',
            'description': 'Calculate return on investment and performance metrics',
            'version': '1.0.0',
            'parameters': {
                'required': ['initial_investment', 'final_value'],
                'optional': ['additional_costs', 'investment_period_months'],
                'initial_investment': {
                    'type': 'decimal',
                    'description': 'Initial amount invested',
                    'min': 0.01
                },
                'final_value': {
                    'type': 'decimal',
                    'description': 'Final or current value of investment',
                    'min': 0
                },
                'additional_costs': {
                    'type': 'decimal',
                    'description': 'Additional costs incurred',
                    'min': 0,
                    'default': 0
                },
                'investment_period_months': {
                    'type': 'integer',
                    'description': 'Duration of investment in months',
                    'min': 1,
                    'max': 1200,
                    'default': None
                }
            },
            'example_request': {
                'initial_investment': 10000,
                'final_value': 15000,
                'additional_costs': 500,
                'investment_period_months': 24
            }
        }
