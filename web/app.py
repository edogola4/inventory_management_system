from flask import Flask, render_template, request, redirect, url_for, flash
from models import Category, Product, init_db
from datetime import datetime

app = Flask(__name__, template_folder='templates')
app.secret_key = 'inventory_pro_secret_key'

# Context processor to inject current datetime into templates
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.route('/')
def index():
    """Home page."""
    category_count = len(Category.get_all())
    product_count = len(Product.get_all())
    return render_template('index.html', category_count=category_count, product_count=product_count)

# Category routes
@app.route('/categories')
def list_categories():
    """List all categories."""
    categories = Category.get_all()
    return render_template('categories/index.html', categories=categories)

@app.route('/categories/new', methods=['GET', 'POST'])
def new_category():
    """Create a new category."""
    if request.method == 'POST':
        try:
            name = request.form['name']
            # Use get() to safely retrieve description; defaults to empty string if missing.
            description = request.form.get('description', '')
            
            if Category.find_by_name(name):
                flash(f"Category '{name}' already exists", "error")
                return render_template('categories/create.html')
            
            category = Category.create(name=name, description=description)
            flash(f"Category '{category.name}' created successfully!", "success")
            return redirect(url_for('list_categories'))
        except ValueError as e:
            flash(str(e), "error")
            return render_template('categories/create.html')
    return render_template('categories/create.html')

@app.route('/categories/<int:id>')
def view_category(id):
    """View a category and its products."""
    category = Category.find_by_id(id)
    if not category:
        flash(f"Category with ID {id} not found", "error")
        return redirect(url_for('list_categories'))
    return render_template('categories/view.html', category=category)

@app.route('/categories/<int:id>/edit', methods=['GET', 'POST'])
def edit_category(id):
    """Edit a category."""
    category = Category.find_by_id(id)
    if not category:
        flash(f"Category with ID {id} not found", "error")
        return redirect(url_for('list_categories'))
    
    if request.method == 'POST':
        try:
            name = request.form['name']
            description = request.form.get('description', '')
            
            # Check if new name is already taken by another category
            existing = Category.find_by_name(name)
            if existing and existing.id != category.id:
                flash(f"Category name '{name}' is already taken", "error")
                return render_template('categories/edit.html', category=category)
            
            # Store the ID before update operation
            category_id = category.id
            
            # Update the category
            category.update(name=name, description=description)
            
            flash("Category updated successfully!", "success")
            # Use the stored ID for the redirect
            return redirect(url_for('view_category', id=category_id))
        except ValueError as e:
            flash(str(e), "error")
    
    return render_template('categories/edit.html', category=category)

@app.route('/categories/<int:id>/delete', methods=['POST'])
def delete_category(id):
    """Delete a category."""
    category = Category.find_by_id(id)
    if not category:
        flash(f"Category with ID {id} not found", "error")
        return redirect(url_for('list_categories'))
    
    try:
        category.delete()
        flash(f"Category '{category.name}' deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting category: {str(e)}", "error")
    
    return redirect(url_for('list_categories'))

# Product routes
@app.route('/products')
def list_products():
    """List all products."""
    products = Product.get_all()
    return render_template('products/index.html', products=products)

@app.route('/products/new', methods=['GET', 'POST'])
def new_product():
    """Create a new product."""
    categories = Category.get_all()
    if not categories:
        flash("No categories available. Please create a category first.", "error")
        return redirect(url_for('new_category'))
    
    if request.method == 'POST':
        try:
            name = request.form['name']
            price = float(request.form['price'])
            quantity = int(request.form['quantity'])
            # Use get() to retrieve description safely.
            description = request.form.get('description', '')
            category_id = int(request.form['category_id'])
            
            if not Category.find_by_id(category_id):
                flash(f"Category with ID {category_id} does not exist", "error")
                return render_template('products/create.html', categories=categories)
            
            product = Product.create(
                name=name,
                price=price,
                quantity=quantity,
                description=description,
                category_id=category_id
            )
            
            flash(f"Product '{product.name}' created successfully!", "success")
            return redirect(url_for('list_products'))
        except (ValueError, TypeError) as e:
            flash(str(e), "error")
    
    return render_template('products/create.html', categories=categories)

@app.route('/products/<int:id>')
def view_product(id):
    """View a product."""
    product = Product.find_by_id(id)
    if not product:
        flash(f"Product with ID {id} not found", "error")
        return redirect(url_for('list_products'))
    return render_template('products/view.html', product=product)

@app.route('/products/<int:id>/edit', methods=['GET', 'POST'])
def edit_product(id):
    """Edit a product."""
    product = Product.find_by_id(id)
    if not product:
        flash(f"Product with ID {id} not found", "error")
        return redirect(url_for('list_products'))
    
    categories = Category.get_all()
    
    if request.method == 'POST':
        try:
            name = request.form['name']
            price = float(request.form['price'])
            quantity = int(request.form['quantity'])
            description = request.form.get('description', '')
            category_id = int(request.form['category_id'])
            
            if not Category.find_by_id(category_id):
                flash(f"Category with ID {category_id} does not exist", "error")
                return render_template('products/edit.html', product=product, categories=categories)
            
            # Store the ID before update
            product_id = product.id
            
            product.update(
                name=name,
                price=price,
                quantity=quantity,
                description=description,
                category_id=category_id
            )
            flash("Product updated successfully!", "success")
            # Use the stored ID for the redirect
            return redirect(url_for('view_product', id=product_id))
        except (ValueError, TypeError) as e:
            flash(str(e), "error")
    
    return render_template('products/edit.html', product=product, categories=categories)

@app.route('/products/<int:id>/delete', methods=['POST'])
def delete_product(id):
    """Delete a product."""
    product = Product.find_by_id(id)
    if not product:
        flash(f"Product with ID {id} not found", "error")
        return redirect(url_for('list_products'))
    
    try:
        product.delete()
        flash(f"Product '{product.name}' deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting product: {str(e)}", "error")
    
    return redirect(url_for('list_products'))

@app.route('/categories/<int:category_id>/products')
def list_products_by_category(category_id):
    """List products by category."""
    category = Category.find_by_id(category_id)
    if not category:
        flash(f"Category with ID {category_id} not found", "error")
        return redirect(url_for('list_categories'))
    
    products = Product.find_by_category(category_id)
    return render_template('products/by_category.html', category=category, products=products)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)