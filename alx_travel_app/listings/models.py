from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Listing(models.Model):
    """
    Model representing a travel listing
    """
    title = models.CharField(max_length=200, help_text="Title of the listing")
    description = models.TextField(help_text="Detailed description of the listing")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Price per night"
    )
    location = models.CharField(max_length=200, help_text="Location of the listing")
    host = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='listings',
        help_text="Host of the listing"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text="Whether the listing is active")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Travel Listing"
        verbose_name_plural = "Travel Listings"
    
    def __str__(self):
        return self.title