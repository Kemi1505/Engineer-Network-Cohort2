from flask import Flask, request, jsonify

app = Flask(__name__)

books = {}
next_id = 1

def validate_book_data(data, is_update=False):
    required_fields = ['title', 'author', 'isbn', 'year']

    if not data:
        return "Request body must be JSON"

    if not is_update:
        for field in required_fields:
            if field not in data:
                return f"Missing field: {field}"

    if 'title' in data and (not isinstance(data['title'], str) or not data['title'].strip()):
        return "Title must be a non-empty string"

    if 'author' in data and (not isinstance(data['author'], str) or not data['author'].strip()):
        return "Author must be a non-empty string"

    if 'isbn' in data and (not isinstance(data['isbn'], str) or not data['isbn'].strip()):
        return "ISBN must be a non-empty string"

    if 'year' in data:
        if not isinstance(data['year'], int):
            return "Year must be an integer"
        if data['year'] < 1000 or data['year'] > 2100:
            return "Year must be between 1000 and 2100"

    return None


# GET /books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(list(books.values())), 200


# GET /books/<id>
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = books.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book), 200


# POST /books
@app.route('/books', methods=['POST'])
def add_book():
    global next_id

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    error = validate_book_data(data)
    if error:
        return jsonify({"error": error}), 400

    # Check duplicate ISBN
    for book in books.values():
        if book['isbn'] == data['isbn']:
            return jsonify({"error": "ISBN already exists"}), 400

    new_book = {
        "id": next_id,
        "title": data['title'],
        "author": data['author'],
        "isbn": data['isbn'],
        "year": data['year']
    }

    books[next_id] = new_book
    next_id += 1

    return jsonify(new_book), 201


# PUT /books/<id>
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    book = books.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json()
    error = validate_book_data(data, is_update=True)
    if error:
        return jsonify({"error": error}), 400

    book.update({
        "title": data.get('title', book['title']),
        "author": data.get('author', book['author']),
        "isbn": data.get('isbn', book['isbn']),
        "year": data.get('year', book['year'])
    })

    return jsonify(book), 200


# DELETE /books/<id>
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    if book_id not in books:
        return jsonify({"error": "Book not found"}), 404

    del books[book_id]
    return jsonify({"message": "Book deleted"}), 200


if __name__ == '__main__':
    app.run(debug=True)
