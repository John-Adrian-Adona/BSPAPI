from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema, TagSchema, TagAndItemSchema

# Use SQLAlchemy
from db import db
from models.store import StoreModel
from models.tag import TagModel
from models.item import ItemModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# Create a blueprint
blp = Blueprint("tags", __name__, description="Operation on tags.")


'''
NEW API Endpoints:
GET  /store/{id}/tag      - Get all tags in a store
POST /store/{id}/tag      - Create a new tag
GET /tag/{id}             - Get information on a tag


POST /item/{tag}/tag/{id} - Link an item in a store with a tag from the same store
DELETE /item/{id}/tag/{id} - Unlink a tag from an item
DELETE /tag/{id} - Delete a tag, which should not have any items that are linked
'''

@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTags(MethodView):
    def post(self, item_id, tag_id):
        # Get the tag and the item rows
        item = ItemModel.query.get_or_404(item_id) # Laptop
        tag = TagModel.query.get_or_404(tag_id)    # Gadget

        # Before linking, we have to make sure that the item and the tag is inside of the same store
        if item.store_id != tag.store_id:
            abort(400, message="Make sure that item and tags belong to the same store before linking.")
        
        # We would add the tag in the 'tags' column of the item
        # Laptop.tags.append("Gadget")
        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while linking the tag and the item")
        
        return {"message": "Tag and Item is succesfully linked."}, 200

    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        # Get the tag and the item rows
        item = ItemModel.query.get_or_404(item_id) 
        tag = TagModel.query.get_or_404(tag_id)  

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while unlinking the item and the tag.")

        return {"message": "Tag removed from the item", "item": item, "tag": tag}
        

@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, req_body, store_id):
        if TagModel.query.filter(
            TagModel.store_id == store_id,
            TagModel.name == req_body["name"]
        ).first():
            abort(400, message="A tag with that name already exists in the same store.")

        # Created a new row/record
        tag = TagModel(name=req_body["name"], store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while creating a tag.")
        
        return tag


@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
    
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if tag.items:
            abort(400, message="Could not delete tag, please unlink all items to this tag before deleting.")
        
        db.session.delete(tag)
        db.session.commit()

        return {"message": "Tag Deleted"}, 200 