from datetime import datetime, time
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def is_restaurant_open():
    """
    Check if the restaurant is currently open based on hardcoded opening hours.

    Returns:
        bool: True if open, False if closed
    """

    # Get current day and time
    now = datetime.now()
    current_time = now.time()
    current_weekday = now.weekday()  # Monday=0, Sunday=6

    # Define opening hours
    # Example: Weekdays 9 AM - 10 PM, Weekends 10 AM - 11 PM
    if current_weekday < 5:  # Monday to Friday
        opening_time = time(9, 0)   # 9:00 AM
        closing_time = time(22, 0)  # 10:00 PM
    else:  # Saturday & Sunday
        opening_time = time(10, 0)  # 10:00 AM
        closing_time = time(23, 0)  # 11:00 PM

    # Check if current time is within opening hours
    if opening_time <= current_time <= closing_time:
        return True
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
        price = float(original_price)
        discount = float(discount_percentage)

        # Check for invalid values
        if price < 0:
            return "Error: Original price cannot be negative."
        if not (0 <= discount <= 100):
            return "Error: Discount percentage must be between 0 and 100."

        # Calculate discounted price
        discounted_price = price * (1 - discount / 100)
        return round(discounted_price, 2)

    except (ValueError, TypeError):
        return "Error: Invalid input. Please provide numeric values."
