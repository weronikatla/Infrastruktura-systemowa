# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@db:5432/booksdb'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(120), unique=False, nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)

    def __repr__(self):
        return '<Book %r>' % self.title

db.create_all()

@app.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'GET':
        books = Book.query.all()
        return jsonify([{'title': book.title, 'author': book.author, 'isbn': book.isbn} for book in books])
    elif request.method == 'POST':
        book = Book(title=request.json['title'], author=request.json['author'], isbn=request.json['isbn'])
        db.session.add(book)
        db.session.commit()
        return jsonify({'success': 'Ksiazka dodana'})

@app.route('/books/<int:book_id>', methods=['GET', 'PUT', 'DELETE'])
def book(book_id):
    book = Book.query.get(book_id)
    if request.method == 'GET':
        return jsonify({'title': book.title, 'author': book.author, 'isbn': book.isbn})
    elif request.method == 'PUT':
        book.title = request.json.get('title', book.title)
        book.author = request.json.get('author', book.author)
        book.isbn = request.json.get('isbn', book.isbn)
        db.session.commit()
        return jsonify({'success': 'Ksiazka zaktualizowana'})
    elif request.method == 'DELETE':
        db.session.delete(book)
        db.session.commit()
        return jsonify({'success': 'Ksiazka usunięta'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
