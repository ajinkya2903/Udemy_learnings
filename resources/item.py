import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, 
                        required='True',
                        help="This field cannot be left blank!")

    parser.add_argument("store_id", type=int, 
                        required='True',
                        help="Every item needs a id!")

    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':"Item is not found"},400


    def post(self,name):
        if ItemModel.find_by_name(name):
            return {"Message":"An item with name {} already exists".format(name)},400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])
        
        try:
            item.save_to_db()
        except:
            {"message":"An error occured while inserting an item"}
    
        return item.json(), 500


    def delete(self,name):
        item=ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        
        return {"message":"Item deleted"}

    def put(self,name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        
        if item is None:
            item = ItemModel(name,**data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()



class ItemList(Resource):
    def get(self):
        return {'items':[x.json() for x in ItemModel.query.all()]}