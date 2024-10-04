from db import db

class ItemModel(db.Model):
    # Table Name
    __tablename__ = "items"

    # Create the fields(columns)
    id = db.Column(db.Integer, primary_key=True)    

    # null - empty (emptyable)
    name = db.Column(db.String(80), nullable=False, unique=True)

    price = db.Column(db.Float(precision=2))

    description = db.Column(db.String(250), nullable=False)

    # unique = False - Repeatable
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)

    # In this relationship, we want this relationship to connect to the StoreModel(stores)
    store = db.relationship("StoreModel", back_populates="items")


    # Add a many to many relationship from item to tags
    # secondary = conjunction table 
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")
