from flask.views import MethodView
from flask_smorest import Blueprint, abort
from uuid import uuid4
from schemas import StoreSchema

# Use SQLAlchemy
from db import db
from models.item import ItemModel
from models.store import StoreModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("stores", __name__, description="Operations on stores endpoint.")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
    
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        db.session.delete(store)
        db.session.commit()

        return {"message": "Store Deleted."}, 200

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, new_store_data):
        store = StoreModel(
            name=new_store_data["name"]
        )

        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while adding the store.")
        except IntegrityError:
            abort(400, message="Store name already exists.")
    
        return store