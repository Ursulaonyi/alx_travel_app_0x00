from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'listings', ListingViewSet)

app_name = 'listings'

urlpatterns = [
    path('', include(router.urls)),
]