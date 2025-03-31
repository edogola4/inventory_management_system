import click
import sys
from models import Category, Product, init_db
from .helpers import (
    print_title, print_table, print_success, print_error, print_info, print_warning,
    confirm_action, get_input, validate_required_string, validate_positive_number,
    validate_positive_integer
)

@click.group()
def cli():
    """InventoryPro CLI - Manage your inventory efficiently."""
    pass

# Category management commands
@cli.group()
def category():
    """Manage product categories."""
    pass

@category.command('list')
def list_categories():
    """List all categories."""
    try:
        print_title("All Categories")
        categories = Category.get_all()
        
        headers = ["ID", "Name", "Description", "Products"]
        rows = []
        
        for cat in categories:
            rows.append([
                cat.id,
                cat.name,
                cat.description or "N/A",
                len(cat.products)
            ])
        
        print_table(headers, rows)
    except Exception as e:
        print_error(f"Failed to list categories: {str(e)}")

@category.command('add')
def add_category():
    """Add a new category."""
    try:
        print_title("Add New Category")
        
        name = get_input("Category name", validate_required_string)
        description = click.prompt("Description (optional)", default="")
        
        if Category.find_by_name(name):
            print_error(f"Category '{name}' already exists")
            return
        
        category = Category.create(name=name, description=description)
        print_success(f"Category '{category.name}' (ID: {category.id}) created successfully")
    except Exception as e:
        print_error(f"Failed to create category: {str(e)}")

@category.command('view')
@click.argument('id', type=int)
def view_category(id):
    """View a category and its products."""
    try:
        category = Category.find_by_id(id)
        if not category:
            print_error(f"Category with ID {id} not found")
            return
        
        print_title(f"Category: {category.name}")
        print_info(f"Description: {category.description or 'N/A'}")
        print_info(f"Number of products: {len(category.products)}")
        
        if category.products:
            print_title("Products in this category")
            headers = ["ID", "Name", "Price", "Quantity", "Description"]
            rows = []
            
            for product in category.products:
                rows.append([
                    product.id,
                    product.name,
                    f"${product.price:.2f}",
                    product.quantity,
                    product.description or "N/A"
                ])
            
            print_table(headers, rows)
        else:
            print_warning("No products in this category")
    except Exception as e:
        print_error(f"Failed to view category: {str(e)}")

@category.command('edit')
@click.argument('id', type=int)
def edit_category(id):
    """Edit a category."""
    try:
        category = Category.find_by_id(id)
        if not category:
            print_error(f"Category with ID {id} not found")
            return
        
        print_title(f"Edit Category: {category.name}")
        
        name = click.prompt("New name", default=category.name)
        description = click.prompt("New description", default=category.description or "")
        
        # Check if the name is already taken by another category
        if name != category.name and Category.find_by_name(name):
            print_error(f"Category name '{name}' is already taken")
            return
        
        category.update(name=name, description=description)
        print_success(f"Category updated successfully")
    except Exception as e:
        print_error(f"Failed to edit category: {str(e)}")

@category.command('delete')
@click.argument('id', type=int)
def delete_category(id):
    """Delete a category and all its products."""
    try:
        category = Category.find_by_id(id)
        if not category:
            print_error(f"Category with ID {id} not found")
            return
        
        product_count = len(category.products)
        
        if product_count > 0:
            warning = f"This will also delete {product_count} product(s) in this category!"
            print_warning(warning)
        
        if confirm_action(f"Are you sure you want to delete '{category.name}'?"):
            category.delete()
            print_success(f"Category '{category.name}' deleted successfully")
        else:
            print_info("Deletion cancelled")
    except Exception as e:
        print_error(f"Failed to delete category: {str(e)}")

# Product management commands
@cli.group()
def product():
    """Manage inventory products."""
    pass

@product.command('list')
def list_products():
    """List all products."""
    try:
        print_title("All Products")
        products = Product.get_all()
        
        headers = ["ID", "Name", "Price", "Quantity", "Category", "Description"]
        rows = []
        
        for prod in products:
            rows.append([
                prod.id,
                prod.name,
                f"${prod.price:.2f}",
                prod.quantity,
                prod.category.name,
                (prod.description[:30] + '...') if prod.description and len(prod.description) > 30 else (prod.description or "N/A")
            ])
        
        print_table(headers, rows)
    except Exception as e:
        print_error(f"Failed to list products: {str(e)}")

@product.command('add')
def add_product():
    """Add a new product."""
    try:
        print_title("Add New Product")
        
        # First check if there are any categories
        categories = Category.get_all()
        if not categories:
            print_error("No categories available. Please create a category first.")
            return
        
        # List available categories
        print_info("Available categories:")
        for cat in categories:
            print_info(f"ID: {cat.id}, Name: {cat.name}")
        
        # Get product details
        name = get_input("Product name", validate_required_string)
        price = get_input("Price ($)", validate_positive_number)
        quantity = get_input("Quantity", validate_positive_integer)
        description = click.prompt("Description (optional)", default="")
        
        # Get category
        category_id = get_input("Category ID", validate_positive_integer)
        
        # Validate category exists
        if not Category.find_by_id(category_id):
            print_error(f"Category with ID {category_id} does not exist")
            return
        
        # Create product
        product = Product.create(
            name=name,
            price=price,
            quantity=quantity,
            description=description,
            category_id=category_id
        )
        
        print_success(f"Product '{product.name}' (ID: {product.id}) created successfully")
    except Exception as e:
        print_error(f"Failed to create product: {str(e)}")

@product.command('view')
@click.argument('id', type=int)
def view_product(id):
    """View details of a product."""
    try:
        product = Product.find_by_id(id)
        if not product:
            print_error(f"Product with ID {id} not found")
            return
        
        print_title(f"Product: {product.name}")
        
        details = [
            ["ID", product.id],
            ["Name", product.name],
            ["Price", f"${product.price:.2f}"],
            ["Quantity", product.quantity],
            ["Category", f"{product.category.name} (ID: {product.category.id})"],
            ["Description", product.description or "N/A"],
            ["Created", product.created_at.strftime("%Y-%m-%d %H:%M:%S")],
            ["Updated", product.updated_at.strftime("%Y-%m-%d %H:%M:%S")]
        ]
        
        print_table(["Attribute", "Value"], details)
    except Exception as e:
        print_error(f"Failed to view product: {str(e)}")

@product.command('edit')
@click.argument('id', type=int)
def edit_product(id):
    """Edit a product."""
    try:
        product = Product.find_by_id(id)
        if not product:
            print_error(f"Product with ID {id} not found")
            return
        
        print_title(f"Edit Product: {product.name}")
        
        # Get updated details
        name = click.prompt("New name", default=product.name)
        price = get_input("New price ($)", lambda x: validate_positive_number(x) if x else product.price, f"Current: ${product.price:.2f}")
        quantity = get_input("New quantity", lambda x: validate_positive_integer(x) if x else product.quantity, f"Current: {product.quantity}")
        description = click.prompt("New description", default=product.description or "")
        
        # List available categories
        categories = Category.get_all()
        print_info("Available categories:")
        for cat in categories:
            print_info(f"ID: {cat.id}, Name: {cat.name}")
        
        current_category = f"Current: {product.category.name} (ID: {product.category_id})"
        category_id = get_input(f"New category ID ({current_category})", 
                               lambda x: validate_positive_integer(x) if x else product.category_id)
        
        # Validate category exists
        if category_id != product.category_id and not Category.find_by_id(category_id):
            print_error(f"Category with ID {category_id} does not exist")
            return
        
        # Update product
        product.update(
            name=name,
            price=price,
            quantity=quantity,
            description=description,
            category_id=category_id
        )
        
        print_success(f"Product updated successfully")
    except Exception as e:
        print_error(f"Failed to edit product: {str(e)}")

@product.command('delete')
@click.argument('id', type=int)
def delete_product(id):
    """Delete a product."""
    try:
        product = Product.find_by_id(id)
        if not product:
            print_error(f"Product with ID {id} not found")
            return
        
        if confirm_action(f"Are you sure you want to delete '{product.name}'?"):
            product.delete()
            print_success(f"Product '{product.name}' deleted successfully")
        else:
            print_info("Deletion cancelled")
    except Exception as e:
        print_error(f"Failed to delete product: {str(e)}")

@product.command('find-by-category')
@click.argument('category_id', type=int)
def find_products_by_category(category_id):
    """Find all products in a category."""
    try:
        category = Category.find_by_id(category_id)
        if not category:
            print_error(f"Category with ID {category_id} not found")
            return
        
        print_title(f"Products in category: {category.name}")
        
        products = Product.find_by_category(category_id)
        
        if not products:
            print_warning(f"No products found in category '{category.name}'")
            return
        
        headers = ["ID", "Name", "Price", "Quantity", "Description"]
        rows = []
        
        for prod in products:
            rows.append([
                prod.id,
                prod.name,
                f"${prod.price:.2f}",
                prod.quantity,
                (prod.description[:30] + '...') if prod.description and len(prod.description) > 30 else (prod.description or "N/A")
            ])
        
        print_table(headers, rows)
    except Exception as e:
        print_error(f"Failed to find products: {str(e)}")

# Initialize database tables
@cli.command('init-db')
def initialize_db():
    """Initialize the database."""
    try:
        init_db()
        print_success("Database initialized successfully")
    except Exception as e:
        print_error(f"Failed to initialize database: {str(e)}")

# Main menu command
@cli.command()
def menu():
    """Show interactive main menu."""
    while True:
        print_title("InventoryPro - Main Menu")
        options = [
            "1. Manage Categories",
            "2. Manage Products",
            "0. Exit"
        ]
        
        for option in options:
            click.echo(option)
        
        choice = click.prompt("Enter your choice", type=int, default=0)
        
        if choice == 0:
            print_info("Exiting InventoryPro. Goodbye!")
            sys.exit(0)
        elif choice == 1:
            category_menu()
        elif choice == 2:
            product_menu()
        else:
            print_error("Invalid choice")

def category_menu():
    """Show category management menu."""
    while True:
        print_title("Category Management")
        options = [
            "1. List all categories",
            "2. Add new category",
            "3. View category details",
            "4. Edit category",
            "5. Delete category",
            "0. Back to main menu"
        ]
        
        for option in options:
            click.echo(option)
        
        choice = click.prompt("Enter your choice", type=int, default=0)
        
        if choice == 0:
            return
        elif choice == 1:
            list_categories()
        elif choice == 2:
            add_category()
        elif choice == 3:
            category_id = get_input("Enter category ID", validate_positive_integer)
            view_category(category_id)
        elif choice == 4:
            category_id = get_input("Enter category ID", validate_positive_integer)
            edit_category(category_id)
        elif choice == 5:
            category_id = get_input("Enter category ID", validate_positive_integer)
            delete_category(category_id)
        else:
            print_error("Invalid choice")

def product_menu():
    """Show product management menu."""
    while True:
        print_title("Product Management")
        options = [
            "1. List all products",
            "2. Add new product",
            "3. View product details",
            "4. Edit product",
            "5. Delete product",
            "6. Find products by category",
            "0. Back to main menu"
        ]
        
        for option in options:
            click.echo(option)
        
        choice = click.prompt("Enter your choice", type=int, default=0)
        
        if choice == 0:
            return
        elif choice == 1:
            list_products()
        elif choice == 2:
            add_product()
        elif choice == 3:
            product_id = get_input("Enter product ID", validate_positive_integer)
            view_product(product_id)
        elif choice == 4:
            product_id = get_input("Enter product ID", validate_positive_integer)
            edit_product(product_id)
        elif choice == 5:
            product_id = get_input("Enter product ID", validate_positive_integer)
            delete_product(product_id)
        elif choice == 6:
            category_id = get_input("Enter category ID", validate_positive_integer)
            find_products_by_category(category_id)
        else:
            print_error("Invalid choice")

if __name__ == '__main__':
    cli()