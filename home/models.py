from django.db import models

# Create your models here.

class Feedback(models.Model):
    "Stores customer feedback"
    comments = models.TextField(help_text="Customer feedback comments.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback #{self.id} - {self.created_at.strftime('%Y-%m-%d')}"

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    # NEW FIELD FOR IMAGE UPLOAD
    image = models.ImageField(
        upload_to='menu_images/',  # Folder inside MEDIA_ROOT
        blank=True,
        null=True,
        help_text='Upload an image of the menu items'
    )

    def __str__(self):
        return self.name