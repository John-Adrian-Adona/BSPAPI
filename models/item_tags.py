from db import db

class ItemsTags(db.Model):
    __tablename__ = "items_tags"

    id = db.Column(db.Integer, primary_key=True)

    # Foreign Keys
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)