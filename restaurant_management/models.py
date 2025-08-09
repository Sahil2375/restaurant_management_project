from django.db import models

class MenuItem(models.Model):
    # Model to represent a restaurant menu item.
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)  # e.g. 8888.88  max

    def __str__(self):
        return self.name