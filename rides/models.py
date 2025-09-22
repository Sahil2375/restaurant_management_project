# Create your models here.

# models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

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
