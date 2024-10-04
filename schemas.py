from marshmallow import Schema, fields


class PlainStoreSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)

class PlainItemSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    description = fields.Str(required=True)

# Create new schema
class PlainTagSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)

class ItemUpdateSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str()
    price = fields.Float()

    store_id = fields.Integer()


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema), dump_only=True)

    # For the new relationship
    tags = fields.List(fields.Nested(PlainTagSchema), dump_only=True)
    
class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True)
    store = fields.Nested(PlainStoreSchema, dump_only=True)

    # Many to Many
    tags = fields.List(fields.Nested(PlainTagSchema), dump_only=True)

# For the new model 
class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema, dump_only=True)

    # Many to Many
    items = fields.List(fields.Nested(PlainItemSchema), dump_only=True)

# Used when unlinking tags to an item
class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True) # POST REQUEST KASMAA (REQ BODY)

# When a schema has a parenthesis, it means that we are going to use it

'''
# CREATE A TAG
# POST - Load
{
    "name": "Electronics",
    "store_id": 1
}

# GET /store/1/tag
# GET - dump
{
    "name": "Electronics",
    "store": {
        "id": 1,
        "name": "Altis Store"
    }
}
'''