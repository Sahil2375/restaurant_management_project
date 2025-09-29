from datetime import datetime, time

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
