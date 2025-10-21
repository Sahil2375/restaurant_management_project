from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Staff

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        read_only_fields = ['username']  # Username should not be editable

class StaffSerializer(serializers.ModelSerializer):
    """
    Serializer for the Staff model.
    Includes all fields.
    """
    class Meta:
        model = Staff
        fields = '__all__'