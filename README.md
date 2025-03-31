# Inventory Management System

A comprehensive inventory management system with both CLI and web browser interfaces.

## Features

- **Product Management**: Add, update, delete, and view products
- **Category Management**: Organize products into categories
- **Transaction Tracking**: Record purchases and sales
- **Supplier Management**: Track supplier information and product relationships
- **Stock Level Alerts**: Get notified when products fall below reorder levels
- **Dual Interface**: Access via command line or web browser

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pipenv install
   ```
3. Initialize the database:
   ```
   pipenv run python -c "from models.base import Base, engine; Base.metadata.create_all(bind=engine)"
   ```

## Usage

### CLI Mode

```
# Run interactive mode
pipenv run python run.py interactive

# List all products
pipenv run python run.py products list-products

# Add a new product
pipenv run python run.py products add-product
```

### Web Mode

```
# Start the web interface
pipenv run python app.py
```

Then open your browser to http://localhost:5000

## Data Model

- **Products**: Core inventory items with details
- **Categories**: Groupings for products
- **Transactions**: Record of inventory movements
- **Suppliers**: Companies that provide products

## Project Requirements

This project fulfills the following requirements:

### ORM Requirements
- Database created and modified with Python ORM methods
- Includes multiple model classes: Product, Category, Transaction, Supplier
- Implements one-to-many relationships:
  - Category to Products
  - Product to Transactions
- Includes property methods with constraints
- Each model class includes ORM methods (create, delete, get all, find by id)

### CLI Requirements
- Interactive menus for user interaction
- Loops to keep user in application until exit
- Complete CRUD operations for each model class
- Input validation with informative error messages

### Project Organization
- Follows OOP best practices
- Proper dependency management with Pipfile
- Organized project structure
- Comprehensive documentation

## License

MIT