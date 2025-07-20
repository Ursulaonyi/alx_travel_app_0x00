# ALX Travel App

A Django-based travel listing platform that allows users to create, manage, and browse travel listings.

## Features

- RESTful API built with Django REST Framework
- MySQL database integration
- Swagger API documentation
- CORS support for frontend integration
- Celery integration for background tasks
- Environment-based configuration
- User authentication and authorization

## Tech Stack

- **Backend**: Django 4.2+
- **API**: Django REST Framework
- **Database**: MySQL
- **Documentation**: Swagger (drf-yasg)
- **Task Queue**: Celery with Redis
- **Environment Management**: django-environ

## Setup Instructions

### Prerequisites

- Python 3.8+
- MySQL 8.0+
- Redis (for Celery)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/alx_travel_app.git
   cd alx_travel_app
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   cd alx_travel_app
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and other settings
   ```

5. **Set up MySQL database:**
   ```sql
   CREATE DATABASE alx_travel_db;
   CREATE USER 'your_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON alx_travel_db.* TO 'your_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

6. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

8. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

## API Documentation

Once the server is running, you can access the API documentation at:

- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/
- **JSON Schema**: http://localhost:8000/swagger.json

## Running Celery (Optional)

To run background tasks:

1. **Start Redis server**

2. **Start Celery worker:**
   ```bash
   celery -A alx_travel_app worker --loglevel=info
   ```

3. **Start Celery beat (for periodic tasks):**
   ```bash
   celery -A alx_travel_app beat --loglevel=info
   ```

## API Endpoints

### Listings

- `GET /api/listings/` - List all listings
- `POST /api/listings/` - Create a new listing (requires authentication)
- `GET /api/listings/{id}/` - Retrieve a specific listing
- `PUT /api/listings/{id}/` - Update a listing (requires authentication)
- `DELETE /api/listings/{id}/` - Delete a listing (requires authentication)
- `GET /api/listings/my_listings/` - Get current user's listings
- `GET /api/listings/featured/` - Get featured listings

### Query Parameters

- `location` - Filter by location (partial match)
- `price_min` - Filter by minimum price
- `price_max` - Filter by maximum price

## Development

### Running Tests

```bash
python manage.py test
```

### Code Style

This project follows PEP 8 style guidelines. You can check your code style using:

```bash
flake8 .
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support, please open an issue in the GitHub repository.