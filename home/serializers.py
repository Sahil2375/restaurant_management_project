from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Rider, Driver, MenuCategory, MenuItem, ContactFormSubmission, UserReview, Restaurant, Table, OpeningHour, Menu

    
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


class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    # category = serializers.StringRelatedField()  # Shows category name instead of ID
    
    class Meta:
        model = MenuItem
        fields = '__all__'  # Include all fields of MenuItem

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be a positive number.")
        return value

class MenuItemAvailabilitySerializer(serializers.Serializer):
    """Serializer to update only availability status"""
    available = serializers.BooleanField()
    
class ContactFormSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactFormSubmission
        fields = ['id', 'name', 'email', 'message', 'submitted_at']
        read_only_fields = ['id', 'submitted_at']

class DailySpecialSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price']

class UserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReview
        fields = ['id', 'user', 'menu_iten', 'rating', 'text', 'review_date']
        read_only_fields = ['id', 'review_date']

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 to 5.")
        return value
    
class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['table_number', 'capacity', 'is_available']


class OpeningHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningHour
        fields = ['day', 'opening_time', 'closing_time']

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'name', 'description', 'price', 'image', 'is_available']
        