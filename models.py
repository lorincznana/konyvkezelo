from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

from flask_login import UserMixin

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(55), unique=True)
    description = db.Column(db.String(255))
    users = db.relationship('User', backref='role', lazy=True)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    borrow_records = db.relationship('BorrowRecord', backref='user', lazy=True)

class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text)

    books = db.relationship('Book', backref='author', lazy=True)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    books = db.relationship('Book', backref='category', lazy=True)

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    isbn = db.Column(db.String(20), unique=True)
    published_year = db.Column(db.Integer)
    available_copies = db.Column(db.Integer, default=1)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    borrow_records = db.relationship('BorrowRecord', backref='book', lazy=True)

class BorrowRecord(db.Model):
    __tablename__ = 'borrow_records'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='borrowed')
