import string
import secrets
import logging
from django.core.mail import send_mail, BadHeaderError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import validate_email
from django.conf import settings
from .models import Order

logger = logging.getLogger(__name__)


def generate_coupon_code(length=10):
    """
    Generate a random alphanumeric coupon code.
    Does not check database uniqueness (model should handle if required).
    """
    characters = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


def generate_unique_order_id(model_class, length=8):
    """
    Generate a unique alphanumeric order_id for a given model.
    Avoids circular imports by passing the model_class explicitly.
    
    Args:
        model_class (Django model): Model class that has an 'order_id' field.
        length (int): Length of the generated order_id string.
    
    Returns:
        str: Unique order_id string.
    """
    characters = string.ascii_uppercase + string.digits

    while True:
        order_id = ''.join(secrets.choice(characters) for _ in range(length))
        if not model_class.objects.filter(order_id=order_id).exists():
            return order_id


def send_order_confirmation_email(order_id, customer_email, customer_name=None):
    """
    Sends an order confirmation email to the customer.
    """
    try:
        validate_email(customer_email)

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

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
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
    """
    try:
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

def calculate_discount(price, discount_percent):
    """
    Calculate discounted price.
    price: Decimal or float
    discount_percent: number (0-100)
    """
    if discount_percent:
        return price * (1 - discount_percent / 100)
    return price


def update_order_status(order_id, new_status):
    """
    Update the status of an order by ID.

    Args:
        order_id (int): ID of the order to update
        new_status (str): New status value (e.g., 'pending', 'processing', 'completed')

    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        order = Order.objects.get(id=order_id)
        old_status = order.status
        order.status = new_status
        order.save()

        # Log the status change
        logger.info(f"Order {order_id} status updated from '{old_status}' to '{new_status}'")

        return True, f"Order {order_id} status updated to '{new_status}'."

    except ObjectDoesNotExist:
        logger.error(f"Order with ID {order_id} not found.")
        return False, f"Order with ID {order_id} not found."

    except Exception as e:
        logger.exception(f"Unexpected error while updating order {order_id}: {str(e)}")
        return False, f"Error updating order {order_id}: {str(e)}"
