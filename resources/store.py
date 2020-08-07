from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message":"Store is not formed!"},404

    def post(self,name):
        if StoreModel.find_by_name(name):
            return {"Store with {} is alraedy exist".format(name)}
        
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message":"An error has occurred"},500

        return store.json(),201

    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        
        return {"message":"store deleted"}

        

class StoreList(Resource):
    def get(self):
        return {'stores':[x.json() for x in StoreModel.query.all()]}