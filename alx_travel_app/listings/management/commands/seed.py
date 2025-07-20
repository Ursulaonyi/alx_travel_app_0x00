import random
from datetime import datetime, timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from listings.models import Listing, Booking, Review


class Command(BaseCommand):
    help = 'Seed the database with sample data for listings, bookings, and reviews'

    def add_arguments(self, parser):
        parser.add_argument(
            '--listings',
            type=int,
            default=20,
            help='Number of listings to create (default: 20)'
        )
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Number of users to create (default: 10)'
        )
        parser.add_argument(
            '--bookings',
            type=int,
            default=50,
            help='Number of bookings to create (default: 50)'
        )
        parser.add_argument(
            '--reviews',
            type=int,
            default=30,
            help='Number of reviews to create (default: 30)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(
                self.style.WARNING('Clearing existing data...')
            )
            self.clear_data()

        # Create users
        users = self.create_users(options['users'])
        self.stdout.write(
            self.style.SUCCESS(f'Created {len(users)} users')
        )

        # Create listings
        listings = self.create_listings(users, options['listings'])
        self.stdout.write(
            self.style.SUCCESS(f'Created {len(listings)} listings')
        )

        # Create bookings
        bookings = self.create_bookings(users, listings, options['bookings'])
        self.stdout.write(
            self.style.SUCCESS(f'Created {len(bookings)} bookings')
        )

        # Create reviews
        reviews = self.create_reviews(bookings, options['reviews'])
        self.stdout.write(
            self.style.SUCCESS(f'Created {len(reviews)} reviews')
        )

        self.stdout.write(
            self.style.SUCCESS('Database seeding completed successfully!')
        )

    def clear_data(self):
        """Clear existing data"""
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Listing.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

    def create_users(self, count):
        """Create sample users"""
        users = []
        
        # Sample user data
        first_names = [
            'John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Chris', 'Anna',
            'Robert', 'Lisa', 'James', 'Maria', 'William', 'Jessica', 'Daniel'
        ]
        last_names = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller',
            'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez'
        ]

        for i in range(count):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            username = f"{first_name.lower()}.{last_name.lower()}.{i}"
            email = f"{username}@example.com"

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                }
            )
            
            if created:
                users.append(user)

        return users

    def create_listings(self, users, count):
        """Create sample listings"""
        listings = []
        
        # Sample listing data
        property_types = [
            'Cozy Apartment', 'Luxury Villa', 'Beach House', 'Mountain Cabin',
            'City Loft', 'Country Cottage', 'Modern Condo', 'Historic Townhouse',
            'Penthouse Suite', 'Garden Bungalow', 'Lakefront Retreat', 'Desert Oasis'
        ]
        
        locations = [
            'New York, NY', 'Los Angeles, CA', 'Miami, FL', 'Chicago, IL',
            'San Francisco, CA', 'Austin, TX', 'Seattle, WA', 'Boston, MA',
            'Denver, CO', 'Atlanta, GA', 'Nashville, TN', 'Portland, OR',
            'Las Vegas, NV', 'Phoenix, AZ', 'San Diego, CA'
        ]
        
        amenities_list = [
            ['WiFi', 'Kitchen', 'Air Conditioning'],
            ['Pool', 'Gym', 'Parking', 'WiFi'],
            ['Beach Access', 'WiFi', 'Kitchen', 'Balcony'],
            ['Mountain View', 'Fireplace', 'Kitchen', 'Parking'],
            ['City View', 'WiFi', 'Elevator', 'Gym'],
            ['Garden', 'BBQ', 'Kitchen', 'Parking', 'Pet Friendly'],
            ['Ocean View', 'Pool', 'Kitchen', 'Beach Access'],
            ['Historic Features', 'WiFi', 'Kitchen', 'Parking']
        ]

        descriptions = [
            "A beautifully designed space perfect for your getaway. Enjoy modern amenities and comfortable accommodations.",
            "Experience luxury and comfort in this stunning property with breathtaking views and top-notch facilities.",
            "Your home away from home with all the essentials for a memorable stay. Clean, comfortable, and convenient.",
            "Immerse yourself in the local culture while enjoying the comfort of this well-appointed accommodation.",
            "Perfect for families or groups, this spacious property offers everything you need for a great vacation."
        ]

        for i in range(count):
            property_type = random.choice(property_types)
            location = random.choice(locations)
            title = f"{property_type} in {location.split(',')[0]}"
            
            # Generate availability dates (next 6 months)
            today = timezone.now().date()
            available_from = today + timedelta(days=random.randint(1, 30))
            available_to = available_from + timedelta(days=random.randint(90, 365))

            listing = Listing.objects.create(
                host=random.choice(users),
                title=title,
                description=random.choice(descriptions),
                location=location,
                price_per_night=Decimal(str(random.randint(50, 500))),
                bedrooms=random.randint(1, 5),
                bathrooms=random.randint(1, 3),
                max_guests=random.randint(2, 10),
                amenities=random.choice(amenities_list),
                available_from=available_from,
                available_to=available_to,
                is_active=random.choice([True, True, True, False])  # 75% active
            )
            
            listings.append(listing)

        return listings

    def create_bookings(self, users, listings, count):
        """Create sample bookings"""
        bookings = []
        status_choices = ['pending', 'confirmed', 'cancelled', 'completed']
        
        # Weight status choices to have more realistic distribution
        status_weights = [0.1, 0.4, 0.1, 0.4]  # More confirmed and completed

        for i in range(count):
            listing = random.choice([l for l in listings if l.is_active])
            guest = random.choice([u for u in users if u != listing.host])
            
            # Generate booking dates within listing availability
            available_days = (listing.available_to - listing.available_from).days
            if available_days < 7:
                continue
                
            start_offset = random.randint(0, available_days - 7)
            check_in_date = listing.available_from + timedelta(days=start_offset)
            duration = random.randint(1, min(14, available_days - start_offset))
            check_out_date = check_in_date + timedelta(days=duration)
            
            # Ensure dates don't exceed availability
            if check_out_date > listing.available_to:
                check_out_date = listing.available_to
                duration = (check_out_date - check_in_date).days
                if duration < 1:
                    continue

            number_of_guests = random.randint(1, min(listing.max_guests, 6))
            total_price = listing.price_per_night * duration
            
            booking_status = random.choices(status_choices, weights=status_weights)[0]
            
            special_requests = [
                "",  # Most bookings don't have special requests
                "Early check-in please",
                "Late check-out if possible",
                "Ground floor room preferred",
                "Quiet room requested",
                "Extra towels needed",
                "Baby crib required"
            ]

            booking = Booking.objects.create(
                listing=listing,
                guest=guest,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                number_of_guests=number_of_guests,
                total_price=total_price,
                booking_status=booking_status,
                special_requests=random.choice(special_requests)
            )
            
            bookings.append(booking)

        return bookings

    def create_reviews(self, bookings, count):
        """Create sample reviews"""
        reviews = []
        
        # Only create reviews for completed bookings
        completed_bookings = [b for b in bookings if b.booking_status == 'completed']
        
        if not completed_bookings:
            self.stdout.write(
                self.style.WARNING('No completed bookings found. Cannot create reviews.')
            )
            return reviews

        review_comments = [
            "Great place to stay! Clean, comfortable, and exactly as described. Would definitely recommend.",
            "Amazing location and beautiful property. The host was very responsive and helpful.",
            "Perfect for our family vacation. Kids loved the amenities and we enjoyed the peaceful atmosphere.",
            "Excellent value for money. Everything we needed was provided and the check-in process was smooth.",
            "Beautiful property with stunning views. A bit remote but that added to the charm.",
            "Good place overall. Could use some minor updates but still a pleasant stay.",
            "Wonderful experience! The property exceeded our expectations. Will definitely book again.",
            "Nice clean space with good amenities. Host was accommodating with our requests.",
            "Lovely place for a romantic getaway. Quiet neighborhood and well-maintained property.",
            "Great location for exploring the city. Easy access to attractions and restaurants."
        ]

        # Create reviews for random selection of completed bookings
        available_bookings = completed_bookings.copy()
        reviews_to_create = min(count, len(available_bookings))
        
        for i in range(reviews_to_create):
            booking = random.choice(available_bookings)
            available_bookings.remove(booking)  # Ensure one review per booking
            
            # Rating distribution weighted towards higher ratings
            rating_choices = [1, 2, 3, 4, 5]
            rating_weights = [0.05, 0.1, 0.15, 0.35, 0.35]  # More 4s and 5s
            rating = random.choices(rating_choices, weights=rating_weights)[0]
            
            review = Review.objects.create(
                listing=booking.listing,
                reviewer=booking.guest,
                booking=booking,
                rating=rating,
                comment=random.choice(review_comments)
            )
            
            reviews.append(review)

        return reviews