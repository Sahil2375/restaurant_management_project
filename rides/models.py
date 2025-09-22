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
    STATUS_CHOICES = [
        ('REQUESTED', 'Requested'),
        ('ONGOING', 'Ongoing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    rider = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='rides', on_delete=models.CASCADE
    )
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='drives', on_delete=models.SET_NULL, null=True, blank=True
    )
    pickup = models.CharField(max_length=255)
    drop = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REQUESTED')
    created_at = models.DateTimeField(auto_now_add=True)

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