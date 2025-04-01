"""
Utility functions for the Inventory Management System.
This package contains various helper functions and utilities.
"""

# Import common functions to make them available at package level
from utils.db import (
    safe_commit,
    execute_query,
    get_or_create,
    bulk_insert,
    paginate_query
)

# You can add version info or other package metadata
__version__ = '0.1.0'