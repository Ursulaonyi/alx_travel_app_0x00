from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from .models import Listing

class ListingModelTest(TestCase):
    """
    Test cases for Listing model
    """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_listing_creation(self):
        """
        Test that a listing can be created successfully
        """
        listing = Listing.objects.create(
            title='Test Listing',
            description='This is a test listing',
            price=Decimal('100.00'),
            location='Test Location',
            host=self.user
        )
        
        self.assertEqual(listing.title, 'Test Listing')
        self.assertEqual(listing.price, Decimal('100.00'))
        self.assertEqual(listing.host, self.user)
        self.assertTrue(listing.is_active)
    
    def test_listing_str_representation(self):
        """
        Test the string representation of a listing
        """
        listing = Listing.objects.create(
            title='Test Listing',
            description='This is a test listing',
            price=Decimal('100.00'),
            location='Test Location',
            host=self.user
        )
        
        self.assertEqual(str(listing), 'Test Listing')

class ListingAPITest(APITestCase):
    """
    Test cases for Listing API endpoints
    """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.listing = Listing.objects.create(
            title='Test Listing',
            description='This is a test listing',
            price=Decimal('100.00'),
            location='Test Location',
            host=self.user
        )
    
    def test_get_listings(self):
        """
        Test retrieving all listings
        """
        response = self.client.get('/api/listings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_single_listing(self):
        """
        Test retrieving a single listing
        """
        response = self.client.get(f'/api/listings/{self.listing.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Listing')
    
    def test_create_listing_requires_authentication(self):
        """
        Test that creating a listing requires authentication
        """
        data = {
            'title': 'New Listing',
            'description': 'This is a new listing',
            'price': '150.00',
            'location': 'New Location'
        }
        response = self.client.post('/api/listings/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)