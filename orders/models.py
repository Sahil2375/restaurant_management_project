from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Menu(models.Model):
    # Menu model representing a dish.
    name = models.CharField(max_length=100)
    description = models.TestField()
    price = models.DecimalField(max_digits=8, decimal_places=2) # e.g. 9999.99 max

    def __str__(self):
        return self.name

class Order(models.Model):
    # Order model representing a customer order.

    STATUS_CHOICES = [
        ('PENDING', Pending),
        ('PREPARING', Preparing),
        ('DELIVERED', Delivered),
        ('CANCELLED', Cancelled),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    order_items = models.ManyToManyField(Menu, related_name="orders")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username}"

    def calculate_total(self):
        # Recalculate the total amount from order items.
        self.total_amount = sum(item.price for item in self.order_items.all())
        self.save()

class UserProfile(models.Model):
    # Extended home profile for storing additional information beyond Django's built-in User model.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class TodaysSpecial(models.Model):
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)  # e.g. 9999.99
    created_at = models.DateTimeField(auto_now_add=True)  # Optional

    def __str__(self):
        return self.item_name