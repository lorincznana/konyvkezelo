from app import app, db
from models import Book

with app.app_context():
    for book in Book.query.all():
        if book.author_id is not None:
            book.author_id += 1  # eggyel növeli, ha el van csúszva
    db.session.commit()

print("Növelve")
