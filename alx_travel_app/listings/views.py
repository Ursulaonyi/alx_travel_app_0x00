from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Listing

# Create a simple serializer for now to avoid import issues
from rest_framework import serializers

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields = ['host', 'created_at', 'updated_at']

# Create your views here.
class ListingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing travel listings
    """
    queryset = Listing.objects.filter(is_active=True)
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        """
        Set the host to the current user when creating a listing
        """
        serializer.save(host=self.request.user)