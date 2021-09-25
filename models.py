import datetime
from enum import unique
from flask_mongoengine import mongoengine as db, Document
from werkzeug.security import generate_password_hash, check_password_hash

class User(Document):
    email = db.StringField(required=True, unique=True)
    password = db.StringField(Required=True)
    subscriptions = db.ListField()
    isAdmin = db.BooleanField(default=False)

    def check_pw(self, password):
        return check_password_hash(self.password, password)

class Feed(Document):
    title = db.StringField(required=True, unique=True)
    url = db.StringField(required=True, unique=True)
    description = db.StringField(required=True)
    added_date = db.DateTimeField(default=datetime.datetime.now())
    added_by = db.ReferenceField(document_type=User)