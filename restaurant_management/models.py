from django.db import models


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