from django.db import models
from django.contrib.auth.models import User

class MenuItem(models.Model):
    # Model to represent a restaurant menu item.
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)  # e.g. 8888.88  max

    def __str__(self):
        return self.name

class RestaurantLocation(models.Model):
    # Stores restaurant location details.
    address = models.CharField(max_length=225)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state} - {self.zip_code}"

class ContactMessage(models.Model):
    # Stores contact form submissions.
    name = models.CharField(max_length=100)
    email = models.EmailField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

class RestaurantInfo(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='restaurant_logos/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True) # New field for address
    description = models.TextField(blank=True, null=True)  # New field for About Us
    # We can add other fields like address, phone etc.

    def __str__(self):
        return self.name
    
class Rider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="rider_profile")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    preferred_payment_method = models.CharField(max_length=50, blank=True, null=True)
    default_pickup_location = models.CharField(max_length=255, blank=True, null=True)
    profile_photo = models.ImageField(upload_to="rider_photos/", blank=True, null=True)

    # Optional future fields: ratings, wallet balance, ride history references etc.
    # wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Rider: {self.user.username}"
    
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="driver_profile")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    vehicle_make = models.CharField(max_length=50, blank=True, null=True)
    vehicle_model = models.CharField(max_length=50, blank=True, null=True)
    number_plate = models.CharField(max_length=20, unique=True, blank=True, null=True)
    license_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    availability_status = models.BooleanField(default=False)  # True if available for rides
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    profile_photo = models.ImageField(upload_to="driver_photos/", blank=True, null=True)

    # Optional future fields: ratings, wallet balance, ride history references etc.
    # wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Driver: {self.user.username}"