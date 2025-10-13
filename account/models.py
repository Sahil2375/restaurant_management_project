from django.db import models
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

# Step 1–3: Create the UserProfile model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_cuisine = models.CharField(
        max_length=50,
        choices=CUISINE_CHOICES,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"