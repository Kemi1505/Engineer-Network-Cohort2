from flask import Flask, request, jsonify
from flask_migrate import Migrate
from database import db
from relationships import Book, Author, Category

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


def serialize_book(book):
    return {
        "id": book.id,
        "title": book.title,
        "isbn": book.isbn,
        "year": book.year,
        "author": book.author.name,
        "category": book.category.name
    }

#Add a book
@app.route('/books', methods=['POST'])
def add_book():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    required = ['title', 'isbn', 'year', 'author', 'category']

    if not all(field in data for field in required):
        return jsonify({"error": "Missing required fields"}), 400

    if not isinstance(data['year'], int):
        return jsonify({"error": "Year must be an integer"}), 400

    if Book.query.filter_by(isbn=data['isbn']).first():
        return jsonify({"error": "ISBN already exists"}), 400

    author = Author.query.filter_by(name=data['author']).first()
    if not author:
        author = Author(name=data['author'])
        db.session.add(author)

    category = Category.query.filter_by(name=data['category']).first()
    if not category:
        category = Category(name=data['category'])
        db.session.add(category)

    book = Book(
        title=data['title'],
        isbn=data['isbn'],
        year=data['year'],
        author=author,
        category=category
    )

    db.session.add(book)
    db.session.commit()

    return jsonify(serialize_book(book)), 201

#Get Book
@app.route('/books', methods=['GET'])
def get_books():
    query = Book.query

    # Search
    search = request.args.get('search')
    if search:
        query = query.join(Author).filter(
            (Book.title.ilike(f"%{search}%")) |
            (Author.name.ilike(f"%{search}%"))
        )

    # Filtering
    year = request.args.get('year')
    if year:
        query = query.filter(Book.year == year)

    category = request.args.get('category')
    if category:
        query = query.join(Category).filter(Category.name == category)

    # Pagination
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)

    books = query.offset(offset).limit(limit).all()
    return jsonify([serialize_book(book) for book in books]), 200

#Get one book
@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(serialize_book(book)), 200

#Update Book
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json()
    book.title = data.get('title', book.title)
    book.year = data.get('year', book.year)

    db.session.commit()
    return jsonify(serialize_book(book)), 200

#Delete Book
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
