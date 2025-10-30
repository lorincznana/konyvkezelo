from flask import Flask, render_template, request, redirect, url_for
from models import db, Author, Book, User, Role, Category
from functools import wraps
import flask
from flask import redirect, url_for, flash
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'T3L1_PULC51_M3L3G3N_T4RT'

#
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'library.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def roles_required(*roles):
    def wrapper(func):
        @wraps(func)
        def decorated_func(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Jelentkezz be a továbbiakhoz.", "warning")
                return redirect(url_for('login'))
            if not current_user.role or current_user.role.name not in [r for r in roles]:
                flash("Nincs jogosultságod ehhez.", "warning")
                return redirect(url_for('index'))
            return func(*args, **kwargs)
        return decorated_func
    return wrapper



@app.route('/')
def index():
    return redirect(url_for('list_authors'))


#-- Author
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/authors')
def list_authors():
    authors = Author.query.all()
    return render_template('authors.html', authors=authors)


@app.route('/authors/new', methods=['GET', 'POST'])
def new_author():
    if request.method == 'POST':
        name = request.form['name']
        bio = request.form['bio']
        author = Author(name=name, bio=bio)
        db.session.add(author)
        db.session.commit()
        return redirect(url_for('list_authors'))
    return render_template('author_form.html', author=None)



@app.route('/authors/edit/<int:id>', methods=['GET', 'POST'])
def edit_author(id):
    author = Author.query.get_or_404(id)
    if request.method == 'POST':
        author.name = request.form['name']
        author.bio = request.form['bio']
        db.session.commit()
        return redirect(url_for('list_authors'))
    return render_template('author_form.html', author=author)

@app.route('/authors/delete/<int:id>')
def delete_author(id):
    author = Author.query.get_or_404(id)
    db.session.delete(author)
    db.session.commit()
    return redirect(url_for('list_authors'))



@app.route('/books')
def list_books():
    books = Book.query.all()
    return render_template('books.html', books=books)




@app.route('/authors/<int:author_id>/books')
def books_by_author(author_id):
    author = Author.query.get_or_404(author_id)
    return render_template('books_by_author.html', author=author)



@app.route('/books/new', methods=['GET', 'POST'])
@login_required
@roles_required('Admin', 'Librarian')
def new_book():
    if request.method == 'POST':
        title = request.form['title']
        isbn = request.form['isbn']
        published_year = request.form['published_year']
        available_copies = request.form['available_copies']
        author_name = request.form['author'].strip()
        category_name = request.form['category'].strip()


        author = Author.query.filter_by(name=author_name).first()
        if not author and author_name:
            author = Author(name=author_name)
            db.session.add(author)
            db.session.commit()


        category = Category.query.filter_by(name=category_name).first()
        if not category and category_name:
            new_category = Category(name=category_name)
            db.session.add(new_category)
            db.session.commit()
            category = new_category


        book = Book(
            title=title,
            isbn=isbn,
            published_year=published_year,
            available_copies=available_copies,
            author_id=author.id if author else None,
            category_id=category.id if category else None
        )

        db.session.add(book)
        db.session.commit()
        flash("Könyv hozzáadva.", "success")
        return redirect(url_for('list_books'))

    return render_template('book_form.html')

@app.route('/books/edit/<int:book_id>')
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    authors = Author.query.all()
    categories = Category.query.all()

    if request.method == 'POST':
        title = request.form['title']  # kérdés
        isbn = request.form['isbn']
        published_year = request.form['published_year']
        available_copies = request.form['available_copies']


        author_name = request.form['author'].strip()
        category_name = request.form['category'].strip()

        author = Author.query.filter_by(name=author_name).first()
        if not author and author_name:
            author = Author(name=author_name)
            db.session.add(author)
            db.session.commit()

        category = Category.query.filter_by(name=category_name).first()
        if not category and category_name:
            category = category(name=category_name)
            db.session.add(category)
            db.session.commit()

        book.author_id = author.id if author else None
        book.category_id = category.id if category else None

        db.session.commit()
        return redirect(url_for('list_books'))

    return render_template('book_form.html', book=book)

@app.route('/books/delete/<int:book_id>')
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('list_books'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            return "A felhasználónév már foglalt."
        if User.query.filter_by(email=email).first():
            return "Ezzel az email-el már regisztráltak."

        user_role=Role.query.filter_by(name="User").first()

        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            role=user_role
        )
        db.session.add(new_user)
        db.session.commit()

        return("Sikeres regisztráció!")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            return "Hibás felhasználónév vagy jelszó!"

        login_user(user)
        return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))





if __name__ == "__main__":
    app.run(debug=True)
