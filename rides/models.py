from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_latitude = models.FloatField(null=True, blank=True)
    current_longitude = models.FloatField(null=True, blank=True)

class Ride(models.Model):
    PAYMENT_METHODS = [
            ('CASH', 'Cash'), 
            ('UPI', 'UPI'), 
            ('CARD', 'Card')
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ONGOING', 'Ongoing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    PAYMENT_STATUS = [
        ('PAID', 'Paid'), 
        ('UNPAID', 'Unpaid')
    ]
    pickup_lat = models.FloatField()
    pickup_lon = models.FloatField()
    drop_lat = models.FloatField()
    drop_lon = models.FloatField()

    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rides")
    fare = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Ride {self.id} - {self.status}"

class RideFeedback(models.Model):
    ride = models.ForeignKey('rides.Ride', on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    is_driver = models.BooleanField()  # True = driver feedback, False = rider feedback
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["ride", "is_driver"], name="unique_feedback_per_role"
            )
        ]