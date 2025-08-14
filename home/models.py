from django.db import models

# Create your models here.

class Feedback(models.Model):
    "Stores customer feedback"
    name = models.CharField(max_length=100)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    # NEW FIELD FOR IMAGE UPLOAD
    image = models.ImageField(
        upload_to='menu_images/',  # Folder inside MEDIA_ROOT/menu_images/
        blank=True,
        null=True,
        help_text='Upload an image of the menu items'
    )

    def __str__(self):
        return self.name

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

class RestaurantInfo(models.Model):
    name = models.CharField(max_length=100)
    address = ,odels.TextField()
    opening_hours = models.JSONField(default=dict)  # e.g. {"Mon": "9am - 10pm", ...}
    phone_number = models.CharField(max_length=20, blank=True)  # New field
    
    def __str__(self):
        return self.name