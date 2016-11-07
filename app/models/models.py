import random
import string
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)

Base = declarative_base()
secret_key = '\x19\xffDM\xbd\x12\x02\xf1\x90ZR\x16`\xfc\x13\xa7^7b\\\x8d5%\x12'


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(40), unique=True)
    password_hash = Column(String(64))

    # Hash Password: DO NOT STORE PASSWORD IN PLAIN TEXT
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    # Verify Password: Compare Password with it's hash
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=300):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})


class BucketList(Base):
    __tablename__ = 'bucketlist'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('user.id'))


class BucketListItems(Base):
    __tablename__ = 'bucketlistitems'
    id = Column(Integer, primary_key=True)
    bucketlist_id = Column(Integer, ForeignKey('bucketlist.id'))
    name = Column(String(100), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.utcnow)
    done = Column(Boolean, default=False)

engine = create_engine('sqlite:///blapi.db')
Base.metadata.create_all(engine)
