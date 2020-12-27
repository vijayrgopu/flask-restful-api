#import sqlite3
from db import db

class ItemModel(db.Model):

    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name 
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price, 'store' : self.store_id}    

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() #you can use cls inplace of the name of a class because its in the same class
        #ItemModel.query.filter_by(name=name).first()

        #if row:
            #return cls(row[0], row[1])
        #    return cls(*row) #parameter unpacking instead of above row[0] and row[1] we use *row because the order is also the same

    def save_to_db(self): #this will update and insert the object into the database
        db.session.add(self)
        db.session.commit()
        '''
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO ITEMS VALUES(?, ?)"
        cursor.execute(query, (self.name, self.price))
        connection.commit()
        connection.close()    
    
    def update(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE ITEMS SET price=? WHERE name=?"
        cursor.execute(query, (self.price,self.name))
        connection.commit()
        connection.close()
        '''
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()   