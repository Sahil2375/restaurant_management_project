import re
from datetime import datetime, time
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from datetime import datetime, time
from .models import Table, DailyOperatingHours

def is_restaurant_open():
    """
    Returns True if the restaurant is currently open based on its operating hours,
    otherwise returns False.
    """

    # Define opening hours (Monday-Friday: 9 AM - 10 PM)
    opening_hours = {
        0: (time(9, 0), time(22, 0)),  # Monday
        1: (time(9, 0), time(22, 0)),  # Tuesday
        2: (time(9, 0), time(22, 0)),  # Wednesday
        3: (time(9, 0), time(22, 0)),  # Thursday
        4: (time(9, 0), time(22, 0)),  # Friday
        5: (time(10, 0), time(20, 0)), # Saturday (optional)
        6: None                        # Sunday (Closed)
    }

    # Get current day and time
    now = datetime.now()
    current_day = now.weekday()  # Monday=0, Sunday=6
    current_time = now.time()

    # Check if today is a working day
    if current_day not in opening_hours or opening_hours[current_day] is None:
        return False  # Closed today

    opening_time, closing_time = opening_hours[current_day]

    # Compare times
    if opening_time <= current_time <= closing_time:
        return True
    else:
        return False



def is_valid_email(email: str) -> bool:
    """
    Validate an email address using Django's built-in validator.
    Returns True if valid, False otherwise.
    """
    try:
        validate_email(email)  # raises ValidationError if invalid
        return True
    except ValidationError:
        return False

def calculate_discount(original_price, discount_percentage):
    """
    Calculate the discounted price for a menu item.

    Args:
        original_price (float or int): The original price of the item.
        discount_percentage (float or int): Discount percentage (0-100).

    Returns:
        float: Discounted price rounded to 2 decimal places.
        str: Error message if inputs are invalid.
    """
    try:
        # Convert inputs to float
        price = float(price)
        discount_percentage = float(discount_percentage)

        # Check for invalid values
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if not (0 <= discount_percentage <= 100):
            raise ValueError("Discount percentage must be between 0 and 100.")

        # Calculate discounted price
        discounted_price = price * (1 - discount_percentage / 100)

        # Return rounded result (2 decimal places)
        return round(discounted_price, 2)

    except (ValueError, TypeError) as e:
        print(f"Error calculating discount: {e}")
        return None


def format_phone_number(phone_number):
    """
    Format a phone number string into a standardized format: (XXX) XXX-XXXX.
    Handles common input variations and errors gracefully.

    :param phone_number: String input representing a phone number
    :return: Formatted phone number as a string or 'Invalid phone number'
    """
    try:
        # Remove all non-digit characters
        digits = re.sub(r'\D', '', phone_number)

        # Handle different lengths
        if len(digits) == 10:
            # e.g., 9876543210 → (987) 654-3210
            formatted = f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits.startswith('1'):
            # e.g., 19876543210 → +1 (987) 654-3210
            formatted = f"+{digits[0]} ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        else:
            return "Invalid phone number"

        return formatted

    except Exception as e:
        print(f"Error formatting phone number: {e}")
        return "Invalid phone number"

def get_available_tables_by_capacity(num_guests):
    """
    Returns a QuerySet of available tables that can accommodate
    the given number of guests.
    
    Filters:
    - is_available is True
    - capacity >= num_guests
    """
    return Table.objects.filter(is_available=True, capacity__gte=num_guests)


def is_restaurant_open_v2():
    """
    Returns True if the restaurant is currently open, False otherwise.
    """
    now = datetime.now()
    current_day = now.strftime('%A')  # e.g., 'Monday', 'Tuesday'
    current_time = now.time()

    try:
        hours = DailyOperatingHours.objects.get(day=current_day)
    except DailyOperatingHours.DoesNotExist:
        # If no hours are set for today, assume closed
        return False

    # Compare current time with opening and closing times
    if hours.opening_time <= current_time <= hours.closing_time:
        return True
    else:
        return False

def format_currency(amount):
    """
    Formats a decimal or float amount as currency with a dollar sign
    and two decimal places.

    Example:
        12.5 -> "$12.50"
    """
    return f"${amount:.2f}"
