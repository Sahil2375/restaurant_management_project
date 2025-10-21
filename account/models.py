from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='restaurant_images/', blank=True, null=True)  # New Field

    def __str__(self):
        return self.name


# Step 4: Define cuisine choices at the top
CUISINE_CHOICES = (
    ('Italian', 'Italian'),
    ('Mexican', 'Mexican'),
    ('Asian', 'Asian'),
    ('Vegetarian', 'Vegetarian'),
)

    
class CustomerProfile(models.Model):
    # Link each profile to a Django user account
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    delivery_address = models.TextField(blank=True, null=True)
    preferred_cuisine = models.CharField(
        max_length=50,
        choices=CUISINE_CHOICES,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.username}'s Customer Profile"
    

class Staff(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
