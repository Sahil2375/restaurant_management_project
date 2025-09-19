# serializers.py
from rest_framework import serializers

class UpdateLocationSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

class TrackRideSerializer(serializers.Serializer):
    driver_latitude = serializers.FloatField()
    driver_longitude = serializers.FloatField()