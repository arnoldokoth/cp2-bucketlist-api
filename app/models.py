from datetime import datetime
from app import db
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

secret_key = '\x19\xffDM\xbd\x12\x02\xf1\x90ZR\x16`\xfc\x13\xa7^7b\\\x8d5%\x12'

__all__ = ['User', 'BucketList', 'BucketListItems']


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password_hash = db.Column(db.String(64))
    bucketlists = db.relationship('BucketList',
                                  backref='',
                                  passive_deletes=True)

    # Hash Password: DO NOT STORE PASSWORD IN PLAIN TEXT
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    # Verify Password: Compare Password with it's hash
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': self.user_id})


class BucketList(db.Model):
    __tablename__ = 'bucketlist'
    bucketlist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow)
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
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow)
    done = db.Column(db.Boolean, default=False)

db.create_all()