from app import app, db
from models import Role, User, Author, Category, Book, BorrowRecord
import os

with app.app_context():
    db.create_all()
    print("Database created successfully!")
    print("Database path:", os.path.abspath("library.db"))
