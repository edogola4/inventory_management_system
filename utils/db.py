# utils/db.py
"""
Database utility functions for the Inventory Management System.
Provides helper functions for common database operations.
"""
import logging
from sqlalchemy.exc import SQLAlchemyError
from models.base import SessionLocal

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_session():
    """
    Get a new database session.
    Should be used as a context manager or with proper closing to avoid leaks.
    
    Returns:
        Session: A new SQLAlchemy session
    """
    return SessionLocal()

def safe_commit(session=None):
    """
    Safely commit changes to the database with error handling.
    
    Args:
        session: SQLAlchemy session object. If None, creates a new session.
    
    Returns:
        bool: True if commit was successful, False otherwise
    """
    close_session = False
    if session is None:
        session = SessionLocal()
        close_session = True
    
    try:
        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Database error during commit: {str(e)}")
        return False
    finally:
        if close_session:
            session.close()

def execute_query(query_func, *args, **kwargs):
    """
    Execute a database query function with proper session handling.
    
    Args:
        query_func: Function that takes a session as first arg and performs query
        *args: Additional arguments to pass to query_func
        **kwargs: Additional keyword arguments to pass to query_func
    
    Returns:
        Query result or None if error occurs
    """
    session = SessionLocal()
    try:
        result = query_func(session, *args, **kwargs)
        return result
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Database error during query: {str(e)}")
        return None
    finally:
        session.close()

def get_or_create(session, model, **kwargs):
    """
    Get an existing record or create it if it doesn't exist.
    
    Args:
        session: SQLAlchemy session
        model: SQLAlchemy model class
        **kwargs: Attributes to filter by and use for creation
    
    Returns:
        Tuple of (instance, created) where created is a boolean
    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.flush()
        return instance, True

def bulk_insert(model_list, chunk_size=100):
    """
    Insert multiple model instances in chunks to improve performance.
    
    Args:
        model_list: List of SQLAlchemy model instances
        chunk_size: Number of records to insert in each transaction
    
    Returns:
        int: Number of successfully inserted records
    """
    if not model_list:
        return 0
    
    session = SessionLocal()
    try:
        total_inserted = 0
        for i in range(0, len(model_list), chunk_size):
            chunk = model_list[i:i + chunk_size]
            session.add_all(chunk)
            session.flush()
            total_inserted += len(chunk)
        session.commit()
        return total_inserted
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Bulk insert error: {str(e)}")
        return 0
    finally:
        session.close()

def paginate_query(query, page=1, per_page=10):
    """
    Paginate a SQLAlchemy query.
    
    Args:
        query: SQLAlchemy query object
        page: Page number (starting from 1)
        per_page: Number of items per page
    
    Returns:
        Tuple of (items, total_pages, total_items)
    """
    if page < 1:
        page = 1
    
    total_items = query.count()
    total_pages = (total_items + per_page - 1) // per_page  # Ceiling division
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    
    return items, total_pages, total_items