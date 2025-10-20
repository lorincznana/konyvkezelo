from flask import Flask, render_template, request, redirect, url_for
from models import db, Author, Book
import os

app = Flask(__name__)

# Mindig az app.py mappájába mentse az adatbázist
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'library.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def index():
    return redirect(url_for('list_authors'))


#-- Author

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


if __name__ == "__main__":
    app.run(debug=True)
