# Create your models here.

# models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_latitude = models.FloatField(null=True, blank=True)
    current_longitude = models.FloatField(null=True, blank=True)

class Ride(models.Model):
    pickup_lat = models.FloatField()
    pickup_lon = models.FloatField()
    drop_lat = models.FloatField()
    drop_lon = models.FloatField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('ONGOING', 'Ongoing'),
            ('COMPLETED', 'Completed'),
            ('CANCELLED', 'Cancelled'),
        ]
    )
    fare = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    payment_status = models.CharField(
        choices=[('PAID', 'Paid'), ('UNPAID', 'Unpaid')],
        default='UNPAID',
        max_length=10
    )
    payment_method = models.CharField(
        choices=[('CASH', 'Cash'), ('UPI', 'UPI'), ('CARD', 'Card')],
        null=True, blank=True,
        max_length=10
    )
    paid_at = models.DateTimeField(null=True, blank=True)

    rider = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='rides', on_delete=models.CASCADE
    )
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='drives', on_delete=models.SET_NULL, null=True, blank=True
    )
    
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