import string
import secrets
from .models import Coupon  # Assuming you have a Coupon model to store codes

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