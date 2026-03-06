"""
Notification Service for Kalkulačky.sk

Handles sending email notifications to users for tracked calculations.
Supports multiple notification types for pregnancy, vacation, mortgage tracking, etc.
"""

from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging
from typing import Optional, Dict, Any


logger = logging.getLogger(__name__)


class NotificationService:
    """
    Service for sending email notifications.
    Supports both plain text and HTML emails with templates.
    """
    
    @staticmethod
    def send_email(
        to_email: str,
        subject: str,
        message: str,
        html_message: Optional[str] = None,
        from_email: Optional[str] = None
    ) -> bool:
        """
        Send email notification.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            message: Plain text message
            html_message: Optional HTML version of the message
            from_email: Optional custom from email (defaults to settings.DEFAULT_FROM_EMAIL)
        
        Returns:
            True if email sent successfully, False otherwise
        """
        if not from_email:
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@kalkulacky.sk')
        
        try:
            if html_message:
                # Send multipart email (plain text + HTML)
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=message,
                    from_email=from_email,
                    to=[to_email]
                )
                email.attach_alternative(html_message, "text/html")
                email.send(fail_silently=False)
            else:
                # Send plain text email
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=from_email,
                    recipient_list=[to_email],
                    fail_silently=False,
                )
            
            logger.info(f"Email sent successfully to {to_email}: {subject}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    @staticmethod
    def send_notification_email(
        to_email: str,
        notification_type: str,
        context: Dict[str, Any],
        calculator_type: str
    ) -> bool:
        """
        Send notification email using pre-defined templates.
        
        Args:
            to_email: Recipient email
            notification_type: Type of notification (e.g., 'pregnancy_week', 'payment_due')
            context: Template context dictionary
            calculator_type: Type of calculator (for template selection)
        
        Returns:
            True if sent successfully, False otherwise
        """
        # Get email subject and template based on notification type
        template_config = NotificationService._get_template_config(
            notification_type,
            calculator_type
        )
        
        if not template_config:
            logger.error(f"No template configuration for {notification_type}")
            return False
        
        subject = template_config['subject'].format(**context)
        
        # Render plain text message
        message = template_config['message'].format(**context)
        
        # Optional: Render HTML template if available
        html_message = NotificationService._render_html_template(
            notification_type,
            calculator_type,
            context
        )
        
        return NotificationService.send_email(
            to_email=to_email,
            subject=subject,
            message=message,
            html_message=html_message
        )
    
    @staticmethod
    def _get_template_config(notification_type: str, calculator_type: str) -> Optional[Dict[str, str]]:
        """
        Get email template configuration for a specific notification type.
        
        Returns:
            Dictionary with 'subject' and 'message' keys, or None if not found
        """
        templates = {
            # ============================================================
            # PREGNANCY NOTIFICATIONS
            # ============================================================
            'pregnancy_week': {
                'subject': '🤰 Týždeň {week} tehotenstva - {calculator_name}',
                'message': (
                    'Ahoj!\n\n'
                    'Vitaj v týždni {week} tehotenstva! 🎉\n\n'
                    '{week_description}\n\n'
                    'Bábätko: {baby_size}\n'
                    'Trimester: {trimester}\n'
                    'Zostáva: {days_remaining} dní do termínu ({due_date})\n\n'
                    '{milestone_message}\n\n'
                    'Zobraziť detail: {action_url}\n\n'
                    'S pozdravom,\n'
                    'Tím Kalkulačky.sk'
                ),
            },
            'pregnancy_milestone': {
                'subject': '🎉 Míľnik tehotenstva - {milestone_name}',
                'message': (
                    'Gratulujeme! 🎊\n\n'
                    'Dosiahli ste dôležitý míľnik vo vašom tehotenstve:\n'
                    '{milestone_name}\n\n'
                    '{milestone_description}\n\n'
                    'Aktuálne: Týždeň {week}, zostáva {days_remaining} dní\n\n'
                    'Zobraziť detail: {action_url}\n\n'
                    'S pozdravom,\n'
                    'Tím Kalkulačky.sk'
                ),
            },
            'trimester_change': {
                'subject': '❤️ Vitajte v {trimester}. trimestri!',
                'message': (
                    'Gratulujeme! 🌟\n\n'
                    'Práve ste vstúpili do {trimester}. trimestra tehotenstva.\n\n'
                    '{trimester_description}\n\n'
                    'Týždeň: {week}\n'
                    'Termín pôrodu: {due_date}\n'
                    'Zostáva: {days_remaining} dní\n\n'
                    'Zobraziť detail: {action_url}\n\n'
                    'Držíme palce!\n'
                    'Tím Kalkulačky.sk'
                ),
            },
            'prenatal_visit': {
                'subject': '🏥 Pripomienka: Prenatálna kontrola',
                'message': (
                    'Ahoj!\n\n'
                    'Je čas na prenatálnu kontrolu.\n\n'
                    'Týždeň tehotenstva: {week}\n'
                    'Odporúčané vyšetrenie: {visit_type}\n\n'
                    '{visit_description}\n\n'
                    'Nezabudnite si dohodnúť termín u vášho lekára.\n\n'
                    'Zobraziť detail: {action_url}\n\n'
                    'S pozdravom,\n'
                    'Tím Kalkulačky.sk'
                ),
            },
            'due_date_approaching': {
                'subject': '🍼 Termín pôrodu sa blíži - {days_remaining} dní!',
                'message': (
                    'Ahoj!\n\n'
                    'Váš termín pôrodu sa rýchlo blíži! 🎉\n\n'
                    'Zostáva: {days_remaining} dní (termín: {due_date})\n'
                    'Týždeň tehotenstva: {week}\n\n'
                    '{preparation_tips}\n\n'
                    'Držíme palce!\n'
                    'Tím Kalkulačky.sk'
                ),
            },
            
            # ============================================================
            # VACATION NOTIFICATIONS
            # ============================================================
            'vacation_expiry': {
                'subject': '🏖️ Dovolenka prepadne o {days_until} dní!',
                'message': (
                    'Ahoj!\n\n'
                    'Pozor! Vaša nevyčerpaná dovolenka prepadne o {days_until} dní.\n\n'
                    'Zostáva: {remaining_days} dní dovolenky\n'
                    'Deadline: {expiry_date}\n\n'
                    'Nezabudnite si ju vyčerpať, aby neprepadla!\n\n'
                    'Zobraziť detail: {action_url}\n\n'
                    'S pozdravom,\n'
                    'Tím Kalkulačky.sk'
                ),
            },
            'vacation_quarterly': {
                'subject': '📅 Štvrťročná kontrola dovolenky',
                'message': (
                    'Ahoj!\n\n'
                    'Čas na kontrolu vašej dovolenky! 🏖️\n\n'
                    'Zostáva: {remaining_days} dní\n'
                    'Vyčerpané: {used_days} dní\n'
                    'Celkovo: {total_days} dní\n\n'
                    '{recommendation}\n\n'
                    'Zobraziť detail: {action_url}\n\n'
                    'S pozdravom,\n'
                    'Tím Kalkulačky.sk'
                ),
            },
            'birthday_33': {
                'subject': '🎂 O {months_until} mesiacov máte 33 rokov - +5 dní dovolenky!',
                'message': (
                    'Ahoj!\n\n'
                    'O {months_until} mesiacov budete mať 33 rokov! 🎉\n\n'
                    'To znamená, že vám pribúda +5 dní dovolenky navyše.\n\n'
                    'Vaša narodeniny: {birthday}\n'
                    'Nová dovolenka od: {effective_date}\n'
                    'Celková dovolenka: {new_total_days} dní\n\n'
                    'Zobraziť detail: {action_url}\n\n'
                    'S pozdravom,\n'
                    'Tím Kalkulačky.sk'
                ),
            },
            'vacation_reminder': {
                'subject': '🏝️ Nezabudnite na dovolenku!',
                'message': (
                    'Ahoj!\n\n'
                    'Zostáva vám ešte {remaining_days} dní dovolenky.\n\n'
                    '{recommendation}\n\n'
                    'Zobraziť detail: {action_url}\n\n'
                    'S pozdravom,\n'
                    'Tím Kalkulačky.sk'
                ),
            },
            
            # ============================================================
            # MORTGAGE/LOAN NOTIFICATIONS
            # ============================================================
            'payment_due': {
                'subject': '💳 Splátka "{calculator_name}" o {days_until} dní',
                'message': (
                    'Ahoj!\n\n'
                    'Pripomienka: Splátka "{calculator_name}" je splatná o {days_until} dní.\n\n'
                    'Suma: {payment_amount} €\n'
                    'Dátum splatnosti: {due_date}\n'
                    'Typ: {loan_type}\n\n'
                    'Nezabudnite mať na účte dostatok prostriedkov.\n\n'
                    'Zobraziť detail: {action_url}\n\n'
                    'S pozdravom,\n'
                    'Tím Kalkulačky.sk'
                ),
            },
            'rate_change': {
                'subject': '📊 Zmena úrokovej sadzby - {calculator_name}',
                'message': (
                    'Ahoj!\n\n'
                    'Zmenila sa úroková sadzba pre váš úver/hypotéku.\n\n'
                    'Predchádzajúca sadzba: {old_rate}%\n'
                    'Nová sadzba: {new_rate}%\n'
                    'Zmena: {rate_change}%\n\n'
                    'Nová mesačná splátka: {new_payment} € (predtým: {old_payment} €)\n\n'
                    '{recommendation}\n\n'
                    'Zobraziť detail: {action_url}\n\n'
                    'S pozdravom,\n'
                    'Tím Kalkulačky.sk'
                ),
            },
            'milestone_paid': {
                'subject': '🎉 Gratulujeme! Splatili ste {percentage}% - {calculator_name}',
                'message': (
                    'Gratulujeme! 🎊\n\n'
                    'Dosiahli ste dôležitý míľnik:\n'
                    'Splatili ste {percentage}% vášho úveru/hypotéky!\n\n'
                    'Splatené: {paid_amount} €\n'
                    'Zostáva: {remaining_amount} €\n'
                    'Celková suma: {total_amount} €\n\n'
                    'Ušetrené na úrokoch: {interest_saved} €\n\n'
                    'Držíme palce!\n'
                    'Tím Kalkulačky.sk'
                ),
            },
            'amortization_alert': {
                'subject': '📉 Amortizačný alert - {calculator_name}',
                'message': (
                    'Ahoj!\n\n'
                    'Tento rok splácate hlavne úroky.\n\n'
                    'Celková ročná splátka: {annual_payment} €\n'
                    'Z toho úroky: {interest_portion} € ({interest_percentage}%)\n'
                    'Z toho istina: {principal_portion} € ({principal_percentage}%)\n\n'
                    '{recommendation}\n\n'
                    'Zobraziť detail: {action_url}\n\n'
                    'S pozdravom,\n'
                    'Tím Kalkulačky.sk'
                ),
            },
            'extra_payment_tip': {
                'subject': '💡 Tip: Nadplatenie ušetrí {savings} € - {calculator_name}',
                'message': (
                    'Ahoj!\n\n'
                    'Máme pre vás tip na úsporu! 💰\n\n'
                    'Ak zaplatíte {extra_amount} € navyše,\n'
                    'ušetríte celkovo {savings} € na úrokoch\n'
                    'a zkrátite dobu splácania o {months_saved} mesiacov.\n\n'
                    'Aktuálny zostatok: {remaining_balance} €\n'
                    'Mesačná splátka: {monthly_payment} €\n\n'
                    'Zobraziť detail: {action_url}\n\n'
                    'S pozdravom,\n'
                    'Tím Kalkulačky.sk'
                ),
            },
            
            # ============================================================
            # GENERIC NOTIFICATION
            # ============================================================
            'generic_reminder': {
                'subject': '{title}',
                'message': (
                    'Ahoj!\n\n'
                    '{message}\n\n'
                    'Zobraziť detail: {action_url}\n\n'
                    'S pozdravom,\n'
                    'Tím Kalkulačky.sk'
                ),
            },
        }
        
        return templates.get(notification_type)
    
    @staticmethod
    def _render_html_template(
        notification_type: str,
        calculator_type: str,
        context: Dict[str, Any]
    ) -> Optional[str]:
        """
        Render HTML email template if available.
        
        Args:
            notification_type: Type of notification
            calculator_type: Type of calculator
            context: Template context
        
        Returns:
            Rendered HTML string, or None if template doesn't exist
        """
        # TODO: Implement HTML template rendering
        # For now, return None (plain text only)
        # In future, create templates in calculators/templates/emails/
        return None
