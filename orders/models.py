from django.db import models
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from home.models import MenuItem  # assuming MenuItem is in home app
from .utils import generate_unique_order_id, calculate_discount


# Create your models here.

class OrderStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., Pending, Preparing, Delivered

    def __str__(self):
        return self.name

class Menu(models.Model):
    # Menu model representing a dish.
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2) # e.g. 9999.99 max

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    # Extended home profile for storing additional information beyond Django's built-in User model.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Special(models.Model):
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)  # e.g. 9999.99
    # created_at = models.DateTimeField(auto_now_add=True)  # Optional

    def __str__(self):
        return self.item_name

class RestaurantInfo(models.Model):
    opening_hours = models.CharField(max_length=225, help_text="e.g. Mon-Fri: 9am-10pm, Sat-Sun: 10am-11pm")

    def __str__(self):
        return "Restaurant Info"
    

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class MenuCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class OrderStatus(models.Model):
    # Model to track status of the order
    name = models.CharField(max_length=50, unique=True)  # e.g. Pending, Preparing, Delivered

    def __str__(self):
        return self.name

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateField()
    valid_until = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code
    
    def is_valid(self):
        """Check if Coupon is active anad within valid dates."""
        today = timezone.now().date()
        return self.is_active and self.valid_from <= today <= self.valid_until
    
class ActiveOrderManager(models.Manager):
    def get_active_orders(self):
        # Only return orders with status 'pending' or 'processing'
        return super().get_queryset().filter(status__in=['pending', 'processing'])

class OrderMAnager(models.Manager):
    def with_status(self, status):
        """Retrieve all orders with a given status."""
        return self.filter(status=status)

    def pending(self):
        """Retrieve all pending orders."""
        return self.with_status("pending")
    
    def processing(self):
        """Retrieve all processing orders."""
        return self.with_status("processing")
    
    def completed(self):
        """Retrieve all completed orders."""
        return self.with_status("completed")
    
    def cancelled(self):
        """Retrieve all cancelled orders."""
        return self.with_status("cancelled")


class Order(models.Model):
    STATUS_CHOICES = [
            ('Pending', 'Pending'),
            ('Processing', 'Processing'),
            ('Completed', 'Completed'),
            ('Cancelled', 'Cancelled'),
        ]
    

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=20, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    customer_name = models.CharField(max_length=100, blank=True, null=True)

    objects = models.Manager()  # The default manager.
    custom = OrderMAnager()  # Our custom manager.

    def save(self, *args, **kwargs):
        if not self.order_id:
            from .utils import generate_unique_order_id
            self.order_id = generate_unique_order_id(Order)
        super().save(*args, **kwargs)

    
    def calculate_total(self):
        from .utils import calculate_discount
        total = 0
        for item in self.items.all():
            total += calculate_discount(item.price, getattr(item, 'discount', 0)) * item.quantity
        return total


    # Attach the custom manager
    objects = ActiveOrderManager()

    def __str__(self):
        return f"Order {self.id} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.CharField(max_length=100)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=1)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # e.g., 10.00 for 10% discount

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"