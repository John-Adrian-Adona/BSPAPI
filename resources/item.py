from flask.views import MethodView
from flask_smorest import Blueprint, abort
from uuid import uuid4
from schemas import ItemSchema, ItemUpdateSchema
from flask_jwt_extended import jwt_required, get_jwt

# Use SQLAlchemy
from db import db
from models.item import ItemModel
from models.store import StoreModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("items", __name__, description="Operations on items endpoint.")

@blp.route("/items/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        # Model.query.get() - always refer to pk
        item = ItemModel.query.get_or_404(item_id)
        return item

    # Only accept fresh tokens
    @jwt_required(fresh=True)
    def delete(self, item_id):
        jwt = get_jwt()

        try:
            if jwt["admin"] == True:
                item = ItemModel.query.get(item_id)

                db.session.delete(item)
                db.session.commit()

                return {"message": "Item deleted."}, 200
        except:
            abort(400, message="You are not an admin.")

    @jwt_required(fresh=True)
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemUpdateSchema)
    def put(self, item_update_data, item_id):
        item = ItemModel.query.get(item_id)

        if item:
            item.name = item_update_data["name"]
            item.price = item_update_data["price"]
        else:
            item = ItemModel(
                name=item_update_data["name"],
                price=item_update_data["price"],
                store_id=item_update_data["store_id"]
            ) 

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while editing the item.")

        return item


@blp.route("/items")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
    
    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, new_item_data):
        # CREATE A NEW RECORD (NOT YET IN THE DATABASE)
        item = ItemModel(
            name=new_item_data["name"],
            price=new_item_data["price"],
            store_id=new_item_data["store_id"]
        )
        
        try:
            # Add the item to the session
            db.session.add(item)
            db.session.commit() # Save to the database
        except SQLAlchemyError:
            abort(500, message="An error occured when creating an Item.")

        return item

