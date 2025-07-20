from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Listing

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for Listing model
    """
    host = UserSerializer(read_only=True)
    host_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'price', 'location', 
            'host', 'host_id', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'host']
    
    def validate_price(self, value):
        """
        Validate that price is positive
        """
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value
    
    def validate_title(self, value):
        """
        Validate that title is not empty and not too long
        """
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty")
        if len(value) > 200:
            raise serializers.ValidationError("Title cannot exceed 200 characters")
        return value.strip()