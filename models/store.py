from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    # ItemModel.store would contain a StoreModel
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete")

    # This would be populated by the TagModel
    tags = db.relationship("TagModel", back_populates="store")


'''
# lazy=dynamic
class AuthorModel(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)

    books = db.relationship("BookModel", back_populates="author", lazy="dynamic", cascade="all, delete")

# foreign key
class BookModel(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    date = db.Column(db.String(255), unique=False, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)

    # Relationship
    author = db.relationship("AuthorModel", back_populates="books")
'''