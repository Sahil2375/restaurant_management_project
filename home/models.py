from django.db import models
from django.utils import timezone
from datetime import timedelta, date
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
    # address = models.TextField()
    description = models.TextField(blank=True, null=True)
    capacity = models.IntegerField(default=0, null=True, blank=True)

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
    name = models.CharField(max_length=100, unique=True)
    # description = models.TextField(blank=True, null=True)
    # category_name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Cuisine(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    cuisine = models.ForeignKey('Cuisine', on_delete=models.SET_NULL, blank=True, null=True)
    discount_percentage = models.PositiveIntegerField(default=0, help_text="Discount in %")
    is_daily_special = models.BooleanField(default=False)  # new field
    available = models.BooleanField(default=True) # Indicates if item is available
    category = models.ForeignKey('MenuCategory', on_delete=models.CASCADE, blank=True, null=True)
    allergens = models.TextField(blank=True, null=True, help_text="List any allergens (e.g., gluten, nuts, dairy)")

    def is_daily_special(self):
        today = date.today()
        return DailySpecial.objects.filter(menu_item=self, date=today).exists()

    def __str__(self):
        return f"{self.name} ({self.allergens})" if self.allergens else self.name

    @classmethod
    def get_items_by_cuisine(cls, cuisine_type):
        """
        Retrieve menu items filtered by the given cuisine type.
        :param cuisine_type: String representing the cuisine (e.g., 'Italian', 'Indian')
        :return: QuerySet of MenuItem objects matching the cuisine type
        """
        return cls.objects.filter(cuisine_type__iexact=cuisine_type, available=True)

    def get_final_price(self) -> float:
        """
        Calculate final price considering discounr.
        Returns float value.
        """
        if self.discount_percentage > 0:
            discount_amount = (self.price * self.discount_percentage) / 100
            final_price = self.price - discount_amount
            return float(final_price)
        return float(self.price)

    
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
    opening_hours = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class DailyOperatingHours(models.Model):
    # Choices for days of the week
    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="operating_hours")
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    class Meta:
        unique_together = ('restaurant', 'day_of_week')  # Ensure one entry per day per restaurant
        ordering = ['day_of_week']

    def __str__(self):
        return f"{self.restaurant.name} - {self.day_of_week}: {self.opening_time} to {self.closing_time}"
    
    def get_total_menu_items(self):
        """
        Returns the total number of menu items associated with this restaurant.
        """
        return self.menuitem_set.count
    

class TodaysSpecial(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class DailySpecial(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = (('menu_item', 'date'),)  # prevent duplicate specials for same item on same day

    def __str__(self):
        return f"{self.menu_item.name} - Special on {self.date}"

    class Meta:
        unique_together = ('menu_item', 'date')  # prevent duplicate specials for same item on same day
        ordering = ['-date']  # latest specials first

    def __str__(self):
        return f"{self.menu_item.name} - {self.date}"
    
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
    rating = models.PositiveIntegerField()
    text = models.TextField(default="")
    review_date = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ('user', 'menu_item')  # prevent duplicate reviews by the same user
    #     ordering = ['-review_date']  # latest reviews first

    def __str__(self):
        return f"Review by {self.user.username} - {self.menu_item.name} ({self.rating}/5)"
    

class Reservation(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    table_number = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Reservation for {self.customer_name} at {self.start_time}"

    @classmethod
    def get_available_slots(cls, start, end, slot_length=timedelta(hours=1), table_number=None):
        """
        Find available reservation slots between 'start' and 'end'.
        
        Args:
            start (datetime): Start of the search window
            end (datetime): End of the search window
            slot_length (timedelta): Length of each slot (default: 1 hour)
            table_number (int, optional): Filter for a specific table

        Returns:
            list of (datetime, datetime): List of available (start, end) slots
        """
        available_slots = []

        # Build all possible slots in the given range
        current = start
        while current + slot_length <= end:
            slot_start = current
            slot_end = current + slot_length

            # Query for overlapping reservations
            reservations = cls.objects.filter(
                start_time__lt=slot_end,
                end_time__gt=slot_start
            )
            if table_number:
                reservations = reservations.filter(table_number=table_number)

            if not reservations.exists():  # slot is free
                available_slots.append((slot_start, slot_end))

            current += slot_length  # move to next slot

        return available_slots


class Table(models.Model):
    number = models.CharField(max_length=10, unique=True)
    capacity = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"Table {self.number} (Capacity: {self.capacity})"


class OpeningHour(models.Model):
    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK, unique=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    def __str__(self):
        return f"{self.get_day_display()}: {self.opening_time} - {self.closing_time}"


class Menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # latest FAQs first
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question
    

class DailyOperatingHours(models.Model):
    day = models.CharField(max_length=20)  # e.g., Monday, Tuesday
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    def __str__(self):
        return f"{self.day}: {self.opening_time} - {self.closing_time}"

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    unit_of_measure = models.CharField(max_length=50)  # e.g., grams, liters

    def __str__(self):
        return self.name