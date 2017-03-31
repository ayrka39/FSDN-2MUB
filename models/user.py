from google.appengine.ext import db
from utils import *


class User(db.Model):
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()

    # get user with userid
    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent=users_key())

    # get user with name
    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    # register by hashing the password first
    @classmethod
    def register(cls, name, pw, email=None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent=users_key(),
                    name=name,
                    pw_hash=pw_hash,
                    email=email)
                    
    # login by checking the password first
    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u