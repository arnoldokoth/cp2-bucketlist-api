import os

from datetime import datetime
from app import app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

secret_key = os.environ['FLASK_SECRET_KEY']
db = SQLAlchemy(app)

__all__ = ['User', 'BucketList', 'BucketListItems']


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password_hash = db.Column(db.String(50))
    bucketlists = db.relationship('BucketList',
                                  backref='',
                                  passive_deletes=True)

    # Hash Password: DO NOT STORE PASSWORD IN PLAIN TEXT
    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Verify Password: Compare Password with it's hash
    def verify_password(self, password):
        return check_password_hash(self.password_hash,password)

    def generate_auth_token(self, expiration=100000000):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': self.user_id})


class BucketList(db.Model):
    __tablename__ = 'bucketlist'
    bucketlist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.now())
    created_by = db.Column(db.Integer, db.ForeignKey('user.user_id',
                                                     ondelete='CASCADE'))
    bucketlistitems = db.relationship('BucketListItems',
                                      backref='bucketlist',
                                      passive_deletes=True)


class BucketListItems(db.Model):
    __tablename__ = 'bucketlistitems'
    item_id = db.Column(db.Integer, primary_key=True)
    bucketlist_id = db.Column(db.Integer,
                              db.ForeignKey('bucketlist.bucketlist_id',
                                            ondelete='CASCADE'))
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.now())
    done = db.Column(db.Boolean, default=False)

# db.create_all()
