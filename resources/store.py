from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message' : 'store not found'}, 404

    def post(self,name):
        if StoreModel.find_by_name(name):
            return {'message' : 'store {} already exists'.format(name)}, 400
        else:
            store = StoreModel(name)
            try:
                store.save_to_db()
            except:
                return {'message' : 'An error occured while saving to db'}, 500
        return store.json(), 201        
                
    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message' : 'store {} has been deleted'.format(name)}


class StoreList(Resource):
    def get(self):
        return {'stores' : [StoreModel.json() for StoreModel in StoreModel.query.all()]}