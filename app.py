from flask import Flask, render_template, request, redirect, url_for
from models import db, Author, Book, User, Role

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'T3L1_PULC51_M3L3G3N_T4RT'

# Mindig az app.py mappájába mentse az adatbázist
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'library.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # ha nincs bejelentkezve, ide küldjük



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
