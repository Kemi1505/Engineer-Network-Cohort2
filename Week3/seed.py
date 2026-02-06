from libraryAPI import app
from database import db
from relationships import Author, Category, Book

with app.app_context():
    author = Author(name="George Orwell")
    category = Category(name="Fiction")

    db.session.add_all([author, category])
    db.session.commit()

    book = Book(
        title="1984",
        isbn="9780451524935",
        year=1949,
        author=author,
        category=category
    )

    db.session.add(book)
    db.session.commit()

    print("Database seeded successfully")
