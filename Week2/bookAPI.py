from flask import Flask, request, jsonify
from datetime import date

app = Flask(__name__)
books = {}
counter = 1

def validate_book_info(data):
    errors = {}
    # checks if data passed is a dictionary(json format)
    if not isinstance(data, dict): 
        errors["JSON_error"] = "Body must be a JSON object"
        return False, errors
    required_fields = {
        "title": str,
        "author": str,
        "year": int,
        "isbn": str
    }
    for field, expected_type in required_fields.items():
        if field not in data:
            errors["Value_error"] = f"Missing {field} field"
        else:
            value = data[field]
            if not isinstance(value, expected_type):
                errors["Type_error"] = f"{field} should be {expected_type.__name__} but got {value.__name__}"
            else:
                if len(str(value).strip()) < 3:
                    errors["error"] = f"{field} cannot be less than 3 characters"
                # strip to remove spaces before and after
                if field == "isbn" and len(str(value).strip()) not in (10, 13):
                    errors["isbn_error"] = "ISBN should be 10 or 13 digits"
                if field == 'year' and not 1000 <= value <= date.today().year:
                    errors["year_error"] = "Year should br between 1000 and current year"
    for book in books:
        if books[book]['isbn'] == data.get('isbn'):
            errors["Duplicate_error"] = "A book with this isbn already exists"

    if (errors):
        return False, errors
    return True, None

@app.route('/books', methods = ['POST'])
def add_book():
    # tell python counter is global
    global counter
    data = request.get_json()
    is_valid, errors = validate_book_info(data)
    if not is_valid:
        return jsonify (errors), 400
    new_book = {
        "id": counter,
        "title": data.get("title"),
        "author": data.get("author"),
        "isbn": data.get("isbn"),
        "year": data.get("year")
    }

    books[counter] = new_book
    counter +=1
    return jsonify (new_book), 201

@app.route('/books', methods = ['GET'])
def get_all_books():
    if len(books) == 0:
        return {"msg": "No book created yet"}
    else:
        return jsonify (books), 200

@app.route('/books/<int:id>', methods = ['GET'])
def get_one_book(id):
    for book in books:
        if book == id:
            return jsonify (books[book]), 200
            
    return {"msg": f"Book with ID {id} does not exist"}, 404
     
@app.route('/books/<int:id>', methods = ['PUT'])
def update_book(id):
    for book in books:
        if book == id:
            data = request.get_json()
            is_valid, errors = validate_book_info(data)
            if not is_valid:
                return jsonify (errors), 400
            updated_book = {
                "id": id,
                "title": data.get("title"),
                "author": data.get("author"),
                "isbn": data.get("isbn"),
                "year": data.get("year")
            }
            books[id] = updated_book
            return jsonify (updated_book),200
    return {"msg": f"Book with ID {id} does not exist"}, 404

@app.route('/books/<int:id>', methods = ['DELETE'])
def delete_book(id):
    for book in books:
        if book == id:
            del books[book]
            return {"msg": f"Book with ID {id} sucessfully deletd"}, 200
    return {"msg": f"Book with ID {id} does not exist"}, 404

if __name__ == "__main__":
    app.run(debug=True)
