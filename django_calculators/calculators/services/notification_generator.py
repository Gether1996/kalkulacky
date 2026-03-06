"""
Notification Generator

Orchestrates the creation of scheduled notifications for tracked calculations.
Uses tracking helpers for different calculator types.
"""

from calculators.models import SavedCalculation, ScheduledNotification
from calculators.services.tracking_helpers import (
    PregnancyTrackingHelper,
    VacationTrackingHelper,
    MortgageLoanTrackingHelper,
)
import logging


logger = logging.getLogger(__name__)


class NotificationGenerator:
    """
    Main notification generator class.
    Delegates to specific tracking helpers based on calculator type.
    """
    
    @staticmethod
    def generate_for_calculation(calculation: SavedCalculation) -> int:
        """
        Generate all scheduled notifications for a saved calculation.
        
        Args:
            calculation: SavedCalculation instance
        
        Returns:
            Number of notifications created
        """
        if not calculation.is_tracking or not calculation.notification_enabled:
            logger.info(f"Tracking disabled for calculation {calculation.id}")
            return 0
        
        # Delete existing notifications for this calculation
        # (in case of re-tracking or parameter changes)
        ScheduledNotification.objects.filter(calculation=calculation).delete()
        
        calculator_type = calculation.calculator_type
        notifications_created = 0
        
        try:
            if calculator_type == 'pregnancy':
                notifications_created = PregnancyTrackingHelper.create_notifications(calculation)
            
            elif calculator_type == 'vacation':
                notifications_created = VacationTrackingHelper.create_notifications(calculation)
            
            elif calculator_type in ['mortgage', 'loan']:
                notifications_created = MortgageLoanTrackingHelper.create_notifications(calculation)
            
            else:
                logger.warning(f"No tracking helper for calculator type: {calculator_type}")
            
            logger.info(
                f"Generated {notifications_created} notifications for calculation {calculation.id} "
                f"({calculator_type})"
            )
        
        except Exception as e:
            logger.error(f"Error generating notifications for calculation {calculation.id}: {e}")
            raise
        
        return notifications_created
    
    @staticmethod
    def regenerate_notifications(calculation: SavedCalculation) -> int:
        """
        Regenerate notifications for a calculation (e.g., after parameter update).
        
        Args:
            calculation: SavedCalculation instance
        
        Returns:
            Number of notifications created
        """
        # Delete existing notifications
        ScheduledNotification.objects.filter(calculation=calculation, sent=False).delete()
        
        # Generate new notifications
        return NotificationGenerator.generate_for_calculation(calculation)
