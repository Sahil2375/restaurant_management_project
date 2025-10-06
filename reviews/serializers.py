from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField()  # shows username instead of ID

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']
