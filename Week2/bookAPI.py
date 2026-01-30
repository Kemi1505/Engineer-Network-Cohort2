from flask import Flask, request, jsonify

app = Flask(__name__)
books = []
book_id = 1

# GET /books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books), 200

# GET /books/<id>
@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    for book in books:
        if book['id'] == id:
            return jsonify(book), 200
    return jsonify({"error": "Book not found"}), 404

# POST /books
@app.route('/books', methods=['POST'])
def add_book():
    global book_id
    data = request.get_json()

    required_fields = ['title', 'author', 'ISBN', 'year']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Fill all required fields"}), 400
    new_book = {
        "id": book_id,
        "title": data['title'],
        "author": data['author'],
        "ISBN": data['ISBN'],
        "year": data['year']
    }
    books.append(new_book)
    book_id += 1
    return jsonify(new_book), 201

# PUT /books/<id>
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()

    for book in books:
        if book['id'] == id:
            book['title'] = data.get('title', book['title'])
            book['author'] = data.get('author', book['author'])
            book['ISBN'] = data.get('ISBN', book['ISBN'])
            book['year'] = data.get('year', book['year'])
            return jsonify(book), 200

    return jsonify({"error": "Book not found"}), 404

# DELETE /books/<id>
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    for book in books:
        if book['id'] == id:
            books.remove(book)
            return jsonify({"message": "Book deleted "}), 200

    return jsonify({"error": "Book not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)