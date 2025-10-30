from app import app, db
from models import Role, User, Author, Category, Book, BorrowRecord
from datetime import datetime, timedelta
import random
from werkzeug.security import generate_password_hash, check_password_hash

with app.app_context():
    db.drop_all()
    db.create_all()

    admin_role = Role(name="Admin", description = "Admin privileges")
    librarian_role = Role(name="Librarian", description = "Librarian privileges")
    user_role = Role(name="User", description = "User privileges")

    db.session.add_all([admin_role, librarian_role, user_role])
    db.session.commit()

    categories = [
        Category(name="Sci-fi"),
        Category(name="True Crime"),
        Category(name="Szépirodalom"),
        Category(name="Romantikus"),
        Category(name="Fantasy")
        ]
    db.session.add_all(categories)
    db.session.commit()

    authors = [
        Author(name="John Pork", bio = "John the Pork"),
        Author(name="J.K. Rowling", bio="A Harry Potter könyvek szerzője."),
        Author(name="George Orwell", bio="Az 1984 és az Állatfarm írója."),
        Author(name="J.R.R. Tolkien", bio="A Gyűrűk Ura szerzője."),
        Author(name="Agatha Christie", bio="Krimiíró, Poirot és Miss Marple történetek megalkotója."),
        ]

    db.session.add_all(authors)
    db.session.commit()

    books = [
        Book(title="Harry Potter és a Bölcsek Köve", isbn="9780747532699", published_year=1997, available_copies=5,
             author=authors[0], category=categories[0]),
        Book(title="1984", isbn="9780451524935", published_year=1949, available_copies=3, author=authors[1],
             category=categories[1]),
        Book(title="A Gyűrűk Ura: A Gyűrű Szövetsége", isbn="9780618260269", published_year=1954, available_copies=4,
             author=authors[2], category=categories[0]),
        Book(title="Gyilkosság az Orient expresszen", isbn="9780007119318", published_year=1934, available_copies=2,
             author=authors[3], category=categories[2]),
    ]

    db.session.add_all(books)
    db.session.commit()

    users = [
        User(username="admin", email="admin@library.hu", password=generate_password_hash("admin123"), role=admin_role),
        User(username="librarian", email="librarian@library.hu", password=generate_password_hash("lib123"),
             role=librarian_role),
        User(username="johndoe", email="john@library.hu", password=generate_password_hash("john123"), role=user_role),
        User(username="janedoe", email="jane@library.hu", password=generate_password_hash("jane123"), role=user_role),
    ]
    db.session.add_all(users)
    db.session.commit()

    borrow_records = [
        BorrowRecord(
            user=users[2],  # johndoe
            book=books[0],
            borrow_date=datetime.utcnow() - timedelta(days=7),
            return_date=None,
            status="borrowed"
        ),
        BorrowRecord(
            user=users[3],  # janedoe
            book=books[1],
            borrow_date=datetime.utcnow() - timedelta(days=30),
            return_date=datetime.utcnow() - timedelta(days=10),
            status="returned"
        ),
    ]
    db.session.add_all(borrow_records)
    db.session.commit()

print("Adatbázis feltöltve mintaadatokkal.")



