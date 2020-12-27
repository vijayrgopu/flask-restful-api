from werkzeug.security import safe_str_cmp
#from resources.user import User
from models.user import UserModel
'''
users = [
    User(1, 'vijay', 'asdf'),
    User(2, 'anusha', 'asdf')
]

username_mapping = {
    u.username : u for u in users
}

userid_mapping = {
    u.id : u for u in users
}
'''

def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    print(payload)
    userid = payload['identity']
    return UserModel.find_by_id(userid)        