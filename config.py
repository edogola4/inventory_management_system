import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_URI = f"sqlite:///{BASE_DIR}/inventory.db"