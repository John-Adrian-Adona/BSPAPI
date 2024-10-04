from db import db

class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique=False, nullable=False) 

    # For every foreign key, there should be a relationship
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)

    # Relationship - ModelName, Column
    store = db.relationship("StoreModel", back_populates="tags")

    # Add a new relationship with item
    # secondary = conjunction table 
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")


# Same name of tags among different stores

'''
Altis Tech Shop - Electronics, Gadgets
Nino Tech Shop  - Electronics, Gadgets

POST /store/1/tag 
{
    "name": "Electronics"
}
'''


'''
# BookGenre - Association table with extra fields (if needed)
class BooksGenres(db.Model):
    __tablename__ = 'books_genres'
    
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.id"), nullable=False)


# Author Model (One Author can write many Books)
class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    books = db.relationship("Book", back_populates="author", lazy="dynamic", cascade="all, delete")

    genres = db.relationship("Genre", back_populates="author", lazy="dynamic", cascade="all, delete")


# Book Model (A Book is written by one Author and can belong to many Genres)
class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)

    # Relationship
    author = db.relationship("Author", back_populates="books")

    genres = db.relationship("Genre", back_populates="books", secondary="books_genres")
    

# Genre Model (A Genre can have many Books and a Book can belong to many Genres)
class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)

    author = db.relationship("Author", back_populates="genres")

    books = db.relationship("Book", back_populates="genres", secondary="books_genres")

'''