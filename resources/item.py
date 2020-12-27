#import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

'''
1. Resource represents items, students, users etc also mapped to database entities
2. API is used to define which CRUD operations can be used against resources
'''
'''
1. Resource class in inherited by the Student class
2. Resource class has Get, Post, Put methods that can be overridden
'''
class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', required=True, type=float, help="price is required")
    parser.add_argument('store_id', required=True, type=int, help="store id is required")

    @jwt_required()
    def get(self,name):
        '''item = next(filter(lambda x : x['name'] == name,items),None)
        return {'item' : item}, 200 if item else 404 '''
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message' : "Item not found"}, 404
    
    def post(self,name):
        if ItemModel.find_by_name(name):
            return {'message' : "Item '{}' already exists".format(name)}, 400
        #data = request.get_json() #use this when you dont intend to use a parser
        data = Item.parser.parse_args()
        item = ItemModel(name,data['price'],data['store_id']) #calls the constructor of the class and creates an ItemModel Object
        try:
            item.save_to_db() #insert method is called on the object of ItemModel
        except:
            return {"message":"An occured inserting"}, 500 #internal server error
        return item.json(), 201

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        
        if item:
            try:
                item.delete_from_db()
            except:    
                return {"message" : "An error Occured"}, 500 #internal server error
            return {"message" : "Item deleted"}, 200  
        return {"message" : "Item not found"}, 404    
    
    def put(self,name):
        #data = request.get_json() #use this when there you dont want to use a parser
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        #updated_item = {'name' : name, 'price' : data['price']}
        if item:
            try:
                item.save_to_db()
            except:
                return {"message":"An error Occured"}, 500    
        else:
            try:
                #item = ItemModel(name, data['price'],data['store_id'])
                item = ItemModel(name, **data)#This is same as the above statement
                item.save_to_db()
            except:
                return {"message":"An error Occured"}, 500    
        return item.json()    
                
class ItemsList(Resource):

    def get(self):
        '''connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM ITEMS"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[1], 'price': row[2]})
        connection.close()'''
        #return {'items' : list(map(lambda x:x.json(),ItemModel.query.all()))}
        #map applies the function x.json to every iterable in the function
        return {'items' : [ItemModel.json() for ItemModel in ItemModel.query.all()]}