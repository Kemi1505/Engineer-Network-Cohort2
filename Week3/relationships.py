from database import db

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    books = db.relationship('Book', backref='author', lazy=True)

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    books = db.relationship('Book', backref='category', lazy=True)

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    isbn = db.Column(db.String(20), nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False)

    author_id = db.Column(
        db.Integer,
        db.ForeignKey('authors.id'),
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id'),
        nullable=False
    )
