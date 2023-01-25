from tinydb import TinyDB, Query
from models import User

db = TinyDB('db.json')
query = Query()


def db_add_user(name: str, password_hash: str, email: str):
    data = {'name': name, 'password_hash': password_hash, 'email': email}
    db.insert(data)


def db_get_user(id: int):
    data = db.get(doc_id=id)
    data.update({'id': data.doc_id})
    return User(**data)

class NoSuchEmailError(Exception):
    pass


def db_get_user_by_email(email: str):
    data = db.get(query.email == email)
    if data:
        data.update({'id': data.doc_id})
        print(data)
        return User(**data)
    else:
        raise NoSuchEmailError


def db_get_all_users():
    data = db.all()
    return [User(**d) for d in data]
