# serializers.py
from rest_framework import serializers
from .models import Ride, Driver

class UpdateLocationSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

class TrackRideSerializer(serializers.Serializer):
    driver_latitude = serializers.FloatField()
    driver_longitude = serializers.FloatField()

class RideHistorySerializer(serializers.ModelSerializer):
    driver = serializers.CharField(source="driver.username", allow_null=True)
    rider = serializers.CharField(source="rider.username", read_only=True)

    class Meta:
        model = Ride
        fields = ['id', 'rider', 'driver', 'pickup', 'drop', 'status', 'created_at']