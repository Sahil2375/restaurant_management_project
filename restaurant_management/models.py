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