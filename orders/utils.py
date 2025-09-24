import string
import secrets
from .models import Coupon  # Assuming you have a Coupon model to store codes

import logging
from django.core.mail import send_mail, BadHeaderError
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.conf import settings

logger = logging.getLogger(__name__)

def generate_coupon_code(length=10):
    """
    Generate a unique alphanumeric coupon code.

    Args:
        length (int): Length of the coupon code. Default is 10.

    Returns:
        str: A unique alphanumeric coupon code.
    """
    alphabet = string.ascii_uppercase + string.digits

    while True:
        # Generate random code
        code = ''.join(secrets.choice(alphabet) for _ in range(length))

        # Check uniqueness in database
        if not Coupon.objects.filter(code=code).exists():
            return code
        


def send_order_confirmation_email(order_id, customer_email, customer_name=None):
    """
    Sends an order confirmation email to the customer.

    Args:
        order_id (int/str): The ID of the order
        customer_email (str): The customer's email address
        customer_name (str, optional): The customer's name for personalization

    Returns:
        dict: { 'success': True/False, 'message': '...' }
    """
    try:
        # Validate email
        validate_email(customer_email)

        # Compose subject and body
        subject = f"Order Confirmation - #{order_id}"
        greeting = f"Hello {customer_name}," if customer_name else "Hello,"
        message = (
            f"{greeting}\n\n"
            f"Thank you for your order!\n"
            f"Your order ID is #{order_id}.\n\n"
            f"We are processing your order and will notify you once it’s shipped.\n\n"
            f"Best regards,\nRestaurant Team"
        )

        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [customer_email]

        # Send the email
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,  # Raise error if email fails
        )

        logger.info(f"Order confirmation email sent to {customer_email} for order #{order_id}")
        return {"success": True, "message": "Email sent successfully."}

    except ValidationError:
        error_message = f"Invalid email address: {customer_email}"
        logger.error(error_message)
        return {"success": False, "message": error_message}

    except BadHeaderError:
        error_message = "Invalid header found while sending email."
        logger.error(error_message)
        return {"success": False, "message": error_message}

    except Exception as e:
        error_message = f"Error sending email: {str(e)}"
        logger.error(error_message, exc_info=True)
        return {"success": False, "message": error_message}


def send_email(recipient_email, subject, message_body, from_email=None):
    """
    Utility function to send an email.
    
    Args:
        recipient_email (str): Recipient email address
        subject (str): Subject of the email
        message_body (str): Body of the email
        from_email (str, optional): Sender email. Defaults to settings.DEFAULT_FROM_EMAIL.
    
    Returns:
        bool: True if email sent successfully, False otherwise.
    """
    try:
        # Validate email format
        validate_email(recipient_email)

        if not from_email:
            from_email = settings.DEFAULT_FROM_EMAIL

        send_mail(
            subject=subject,
            message=message_body,
            from_email=from_email,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        return True

    except ValidationError:
        print(f"Invalid email address: {recipient_email}")
        return False
    except BadHeaderError:
        print("Invalid header found.")
        return False
    except Exception as e:
        print(f"Error sending email: {e}")
        return False