# ALX Travel App 0x00 - Database Modeling and Data Seeding

This Django application implements a travel booking system with comprehensive database models, API serializers, and data seeding capabilities.

## Project Structure

```
alx_travel_app_0x00/
├── alx_travel_app/
│   ├── listings/
│   │   ├── models.py              # Database models
│   │   ├── serializers.py         # DRF serializers
│   │   └── management/
│   │       └── commands/
│   │           └── seed.py        # Database seeding command
│   └── ...
└── README.md
```

## Models

### Listing Model
- **Primary Key**: UUID field (`listing_id`)
- **Host**: Foreign key to User model
- **Core Fields**: title, description, location, price_per_night
- **Property Details**: bedrooms, bathrooms, max_guests
- **Features**: amenities (JSON field), availability dates
- **Status**: is_active, timestamps
- **Methods**: `average_rating` property

### Booking Model
- **Primary Key**: UUID field (`booking_id`)
- **Relationships**: Foreign keys to Listing and User (guest)
- **Booking Details**: check-in/out dates, number of guests
- **Pricing**: total_price calculation
- **Status**: pending, confirmed, cancelled, completed
- **Features**: special_requests, validation methods
- **Properties**: `duration_days` calculation

### Review Model
- **Primary Key**: UUID field (`review_id`)
- **Relationships**: Foreign keys to Listing, User (reviewer), and optional Booking
- **Content**: rating (1-5), comment
- **Constraints**: Unique per listing-reviewer combination
- **Validation**: Ensures reviewer has completed booking

## Serializers

### ListingSerializer
- Basic listing information with host details
- Read-only average rating calculation
- Custom validation for availability dates

### ListingDetailSerializer
- Extended listing serializer with reviews
- Includes recent reviews and review count
- Optimized for detailed views

### BookingSerializer
- Complete booking information
- Includes related listing and guest data
- Duration calculation and validation

### BookingCreateSerializer
- Streamlined booking creation
- Automatic price calculation
- Comprehensive validation including availability checks

### ReviewSerializer
- Review display with reviewer information
- Rating validation (1-5 range)

### ReviewCreateSerializer
- Review creation with business logic validation
- Ensures only guests with completed bookings can review
- Prevents duplicate reviews

## Database Seeding

The `seed.py` management command populates the database with realistic sample data:

### Features
- **Configurable Quantities**: Specify number of users, listings, bookings, and reviews
- **Realistic Data**: Uses proper names, locations, and descriptions
- **Relationship Integrity**: Ensures proper foreign key relationships
- **Business Logic**: Respects booking constraints and review requirements
- **Data Cleaning**: Option to clear existing data before seeding

### Usage

```bash
# Basic seeding with default quantities
python manage.py seed

# Custom quantities
python manage.py seed --listings 50 --users 20 --bookings 100 --reviews 75

# Clear existing data and reseed
python manage.py seed --clear

# Help with all options
python manage.py seed --help
```

### Sample Data Generated

**Users**: 
- Realistic first/last name combinations
- Unique usernames and email addresses
- Mix of hosts and guests

**Listings**:
- Diverse property types (apartments, villas, cabins, etc.)
- Major US cities as locations
- Varied amenities (WiFi, pools, kitchens, etc.)
- Realistic pricing ($50-$500 per night)
- Different property sizes (1-5 bedrooms)
- 75% active listings

**Bookings**:
- Realistic date ranges within listing availability
- Proper guest capacity validation
- Weighted status distribution (more confirmed/completed)
- Optional special requests
- Calculated total pricing

**Reviews**:
- Only for completed bookings
- Weighted toward higher ratings (4-5 stars)
- Diverse, realistic comments
- One review per booking maximum

## Database Indexes

Performance optimizations included:

- **Listings**: location, price_per_night, availability dates
- **Bookings**: booking dates, status
- **Reviews**: rating

## Model Relationships

```
User (Django Auth)
├── listings (1:N) → Listing
├── bookings (1:N) → Booking  
└── reviews (1:N) → Review

Listing
├── bookings (1:N) → Booking
└── reviews (1:N) → Review

Booking
└── review (1:1) → Review
```

## Validation Rules

### Booking Validation
- Check-out date must be after check-in date
- Guest count cannot exceed listing maximum
- Booking dates must be within listing availability
- Only active listings can be booked

### Review Validation
- Rating must be between 1-5
- Only guests with completed bookings can review
- One review per listing per user
- Reviewer must be the booking guest

## Installation and Setup

1. **Duplicate the project**:
   ```bash
   cp -r alx_travel_app alx_travel_app_0x00
   cd alx_travel_app_0x00
   ```

2. **Install dependencies**:
   ```bash
   pip install django djangorestframework
   ```

3. **Add to Django settings**:
   ```python
   INSTALLED_APPS = [
       # ... other apps
       'rest_framework',
       'listings',
   ]
   ```

4. **Create and run migrations**:
   ```bash
   python manage.py makemigrations listings
   python manage.py migrate
   ```

5. **Create management command directory**:
   ```bash
   mkdir -p listings/management/commands
   touch listings/management/__init__.py
   touch listings/management/commands/__init__.py
   ```

6. **Seed the database**:
   ```bash
   python manage.py seed
   ```

## Key Features

### Models
- **UUID Primary Keys**: Enhanced security and scalability
- **Comprehensive Validation**: Custom clean() methods and field validators
- **Optimized Queries**: Strategic database indexes
- **Rich Relationships**: Proper foreign keys and related names

### Serializers
- **Nested Serialization**: Related object details in responses
- **Custom Validation**: Business logic enforcement
- **Flexible Creation**: Separate serializers for create/read operations
- **Calculated Fields**: Dynamic property inclusion

### Data Seeding
- **Realistic Data**: Proper names, locations, and relationships
- **Configurable Scale**: Adjustable quantities for testing
- **Business Logic**: Respects all model constraints
- **Performance Aware**: Efficient bulk operations

## API Integration Ready

The serializers are designed for immediate integration with Django REST Framework views:

- **CRUD Operations**: Full create, read, update, delete support
- **Filtering Ready**: Optimized for search and filter operations  
- **Pagination Friendly**: Efficient queries for large datasets
- **Authentication Aware**: User context handling built-in

## Development Notes

- All models use UUID primary keys for enhanced security
- JSON fields store amenities for flexible property features  
- Timestamps are automatically managed
- Foreign key relationships use descriptive related names
- Custom validation ensures data integrity
- Indexes optimize common query patterns

This implementation provides a solid foundation for a travel booking platform with proper data modeling, API serialization, and comprehensive sample data generation.