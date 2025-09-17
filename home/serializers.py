from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Rider, Driver


class UserSerializer(serializers.ModelSerializer):
    """Basic user serializer to embed in Rider/Driver responses."""

    class Meta:
        model = User
        fields = ("id", "username", "email")


class RiderRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = Rider
        fields = (
            "username",
            "email",
            "password",
            "phone_number",
            "preferred_payment_method",
            "default_pickup_location",
        )

    def create(self, validated_data):
        username = validated_data.pop("username")
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        # create user
        user = User.objects.create_user(username=username, email=email, password=password)

        # create rider profile
        rider = Rider.objects.create(user=user, **validated_data)
        return rider

    def to_representation(self, instance):
        return {
            "user": UserSerializer(instance.user).data,
            "phone_number": instance.phone_number,
            "preferred_payment_method": instance.preferred_payment_method,
            "default_pickup_location": instance.default_pickup_location,
        }


class DriverRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = Driver
        fields = (
            "username",
            "email",
            "password",
            "phone_number",
            "license_number",
            "vehicle_make",
            "vehicle_model",
            "number_plate",
        )

    def create(self, validated_data):
        username = validated_data.pop("username")
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        # create user
        user = User.objects.create_user(username=username, email=email, password=password)

        # create driver profile
        driver = Driver.objects.create(user=user, **validated_data)
        return driver

    def to_representation(self, instance):
        return {
            "user": UserSerializer(instance.user).data,
            "phone_number": instance.phone_number,
            "license_number": instance.license_number,
            "vehicle_make": instance.vehicle_make,
            "vehicle_model": instance.vehicle_model,
            "number_plate": instance.number_plate,
            "availability_status": instance.availability_status,
        }
