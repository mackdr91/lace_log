# Sneaker Inventory Management System

This Django-based web application allows users to manage their sneaker collections and inventory. Users can create profiles, add sneakers to their inventory, manage variations, and organize sneakers into collections.

## Features

- User authentication and profile management
- Sneaker inventory management
- Sneaker variations (size and quantity)
- Collection organization
- QR code generation for sneakers

## Project Structure

The project consists of two main Django apps:

1. `core`: Handles user profiles
2. `inventory`: Manages sneakers, variations, and collections

### Core Models

- `Profile`: Extends the default Django User model with additional fields like bio, location, and profile picture.

### Inventory Models

- `Sneaker`: Represents individual sneakers with details such as name, brand, price, release date, etc.
- `SneakerVariation`: Manages different sizes and quantities for each sneaker.
- `Collection`: Allows users to organize sneakers into collections.

## Installation

1. Clone the repository
2. Create a virtual environment and activate it
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```
   python manage.py migrate
   ```
5. Start the development server:
   ```
   python manage.py runserver
   ```

## Usage

(Add instructions on how to use the application, create users, add sneakers, etc.)

## Dependencies

- Django
- Pillow (for image handling)
- Tailwind CSS
- QRCode
- Docker
- Docker Compose
- SQL


## Contributing

(Add instructions for contributing to the project if it's open-source)

## License

(Add license information)
