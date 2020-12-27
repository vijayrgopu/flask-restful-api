from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemsList
from resources.store import Store, StoreList
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #trying to use sqlalchemy track modifications rather than the Flask App one
app.secret_key='vgopu'
api = Api(app)
db.init_app(app)

'''endpoint /auth'''
jwt = JWT(app, authenticate, identity)

#This will create all db tables before a first request is called
@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Store,'/store/<string:name>')
api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemsList,'/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister,'/register')


#When importing a file such as eg. "from item import Item" then python usually runs the .py script behind the scenes,
#it is ok to have it that way if there are no commands that run the application such as eg. app.run() because you dont want to run 
#the app while importing but while executing so we use "if __name__ == 'main'" to overcome this issue
if __name__ == '__main__':   
    app.run(port=5000, debug=True)