from libraryAPI import app
from database import db
from relationships import Author, Category, Book

with app.app_context():
    author = Author(name="Chimamanda Ngozi Adichie")
    category = Category(name="Fiction")

    db.session.add_all([author, category])
    db.session.commit()

    book = Book(
        title="Americanah",
        isbn="9780307455925",
        year=2013,
        author=author,
        category=category
    )

    db.session.add(book)
    db.session.commit()

    print("Database seeded successfully")
