from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Feedback(models.Model):
    "Stores customer feedback"
    name = models.CharField(max_length=100)
    feedback_text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.name}"


class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

class RestaurantInfo(models.Model):
    name = models.CharField(max_length=100, default="My Restaurant")
    address = models.TextField()
 
    def __str__(self):
        return self.name

class Chef(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to="chefs/")

    def __str__(self):
        return self.name

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
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
    
class MenuCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, default="General")
    description = models.TextField(blank=True, null=True)
    category_name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name
    
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_daily_special = models.BooleanField(default=False)  # new field
    available = models.BooleanField(default=True)
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name="menu_items")

    def __str__(self):
        return self.name
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
    
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # New field for operating days
    operating_days = models.CharField(
        max_length=50, # enough for comma-separated days
        default="Mon, Tue, Wed, Thurs, Fri, Sat, Sun",
        help_text="Comma-separated days (e.g., Mon, Tue, Wed, Thurs, Fri, Sat, Sun)",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name
    

class TodaysSpecial(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class ContactFormSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)  # Tract when form is submitted

    def __str__(self):
        return f"{self.name} - {self.email}"
    
class UserReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField()
    comment = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'menu_item')  # prevent duplicate reviews by the same user
        ordering = ['-review_date']  # latest reviews first

    def __str__(self):
        return f"{self.user.username} - {self.menu_item.name} ({self.rating}/5)"