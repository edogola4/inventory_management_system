# services/product_service.py
from models.product import Product
from sqlalchemy.orm import Session

class ProductService:
    def __init__(self, session: Session):
        self.session = session
        
    def create_product(self, name, description, category, quantity, cost_price, selling_price, reorder_level=0):
        """Create a new product."""
        product = Product(
            name=name,
            description=description,
            category=category,
            quantity=quantity,
            cost_price=cost_price,
            selling_price=selling_price,
            reorder_level=reorder_level
        )
        self.session.add(product)
        self.session.commit()
        return product
    
    def get_product(self, product_id):
        """Get product by ID."""
        return self.session.query(Product).get(product_id)
    
    def get_all_products(self):
        """Get all products."""
        return self.session.query(Product).all()
    
    def get_products_by_category(self, category):
        """Get all products in a specific category."""
        return self.session.query(Product).filter(Product.category == category).all()
    
    def get_low_stock_products(self):
        """Get products with quantity below reorder level."""
        return self.session.query(Product).filter(Product.quantity <= Product.reorder_level).all()
    
    def update_product(self, product_id, **kwargs):
        """Update product properties."""
        product = self.get_product(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} does not exist")
        
        for key, value in kwargs.items():
            if hasattr(product, key):
                setattr(product, key, value)
        
        self.session.commit()
        return product
    
    def delete_product(self, product_id):
        """Delete a product."""
        product = self.get_product(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} does not exist")
        
        self.session.delete(product)
        self.session.commit()