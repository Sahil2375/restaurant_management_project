import string
import secrets
import logging
from datetime import date
from django.db.models import Sum
# from .models import Order
from django.core.mail import send_mail, BadHeaderError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import validate_email
from django.conf import settings

logger = logging.getLogger(__name__)


def generate_coupon_code(length=10):
    """
    Generate a random alphanumeric coupon code.
    Does not check database uniqueness (model should handle if required).
    """
    characters = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


def generate_unique_order_id(model_class, length=8):
    from .models import Order
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
        return secrets.token_hex(length // 2)


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

def calculate_discount(order_total, discount_percentage):
    """
    Calculate the discount amount for an order.

    Args:
        order_total (float or int): The total amount of the order.
        discount_percentage (float or int): Discount percentage (0-100).

    Returns:
        float: The discount amount.
        str: Error message if input is invalid.

    Usage:
        >>> calculate_discount(500, 10)
        50.0

        >>> calculate_discount(100, 120)
        'Error: Discount percentage must be between 0 and 100.'
    """
    try:
        order_total = float(order_total)
        discount_percentage = float(discount_percentage)
    except (ValueError, TypeError):
        return "Error: Invalid input. Please provide numeric values."

    if not (0 <= discount_percentage <= 100):
        return "Error: Discount percentage must be between 0 and 100."

    discount_amount = order_total * (discount_percentage / 100)
    return round(discount_amount, 2)



def update_order_status(order_id, new_status):
    from .models import Order   # 👈 local import avoids circular import
    
    try:
        order = Order.objects.get(id=order_id)
        old_status = order.status
        order.status = new_status
        order.save()

        logger.info(f"Order {order_id} status updated from '{old_status}' to '{new_status}'")
        return True, f"Order {order_id} status updated to '{new_status}'."

    except ObjectDoesNotExist:
        logger.error(f"Order with ID {order_id} not found.")
        return False, f"Order with ID {order_id} not found."

    except Exception as e:
        logger.exception(f"Unexpected error while updating order {order_id}: {str(e)}")
        return False, f"Error updating order {order_id}: {str(e)}"

def calculate_order_total(order_items):
    """
    Calculate the total price of an order.

    Args:
        order_items (list of dict): 
        A list where each item is a dictionary containing 'quantity' (int/float) and 'price' (int/float).
        Example: [{'quantity': 2, 'price': 50}, {'quantity': 1, 'price': 100}]

    Returns:
        float: The total cost of the order. Returns 0.0 if the list is empty.
    """
    if not order_items:  # Handle empty list gracefully
        return 0.0

    total = 0.0
    for item in order_items:
        # Safely get quantity and price with defaults
        quantity = item.get("quantity", 0)
        price = item.get("price", 0.0)

        # Ensure values are valid numbers
        try:
            total += float(quantity) * float(price)
        except (ValueError, TypeError):
            continue  # skip invalid items instead of crashing

    return round(total, 2)  # rounded to 2 decimal places for currency format


def get_daily_sales_total(specific_date: date):
    """
    Calculate total sales for a specific date by summing total_price of all orders.

    Args:
        specific_date (date): The date for which to calculate total sales.

    Returns:
        Decimal or float: Total sales amount for the date. Returns 0 if no orders exist.
    """
    # Filter orders by the given date
    orders = Order.objects.filter(created_at__date=specific_date)

    # Aggregate total price
    total = orders.aggregate(total_sum=Sum('total_price'))['total_sum']

    # Return 0 if no orders exist
    return total or 0


def calculate_average_rating(reviews_queryset):
    """
    Calculate the average rating from a queryset of reviews.

    :param reviews_queryset: Django queryset of Review objects
    :return: Float representing the average rating, or 0.0 if no reviews
    """
    try:
        total_reviews = reviews_queryset.count()

        # Handle case when there are no reviews
        if total_reviews == 0:
            return 0.0

        total_rating = sum(review.rating for review in reviews_queryset)
        average_rating = total_rating / total_reviews

        return round(average_rating, 2)  # Rounded to 2 decimal places
    except Exception as e:
        # Log or handle unexpected errors gracefully
        print(f"Error calculating average rating: {e}")
        return 0.0


def calculate_estimated_prep_time(order_items):
    """
    Calculate the total estimated preparation time for an order.

    Args:
        order_items (list): A list of dictionaries, where each dictionary contains:
            - 'menu_item_id' (int): The ID of the menu item.
            - 'quantity' (int): The number of that item ordered.
            - 'prep_time_minutes' (int): The preparation time for one unit of the item.

            Example:
            [
                {'menu_item_id': 1, 'quantity': 2, 'prep_time_minutes': 10},
                {'menu_item_id': 5, 'quantity': 1, 'prep_time_minutes': 15}
            ]

    Returns:
        int: The total estimated preparation time in minutes.
    """

    total_prep_time = 0

    for item in order_items:
        # Safely extract fields with defaults to handle missing keys
        quantity = item.get('quantity', 1)
        prep_time = item.get('prep_time_minutes', 0)

        total_prep_time += quantity * prep_time

    return int(total_prep_time)
