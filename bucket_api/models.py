import datetime
from marshmallow import Schema, fields, pre_load
from marshmallow import validate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask import Flask, jsonify, json, g
from sqlalchemy import Column, INTEGER, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from bucket_api.config import Config

db = SQLAlchemy()
marshmallow = Marshmallow()
auth = HTTPBasicAuth()
tokenization = HTTPTokenAuth()

class AddUpdateDelete:
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()


class User(db.Model, AddUpdateDelete):
    """ users table"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    fullname = db.Column(db.String(50))
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    date_created = db.Column(db.DateTime, server_default=func.now())
    bucketlists = db.relationship('BucketList', backref='users', cascade='all, delete', lazy='dynamic')

    @property
    def password(self):
        """ Prevent password from being accessed """

        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """ Set a hashed password """

        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """ Check hashed password matches actual password """

        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=43200):

        s = Serializer(Config.SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.user_id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(Config.SECRET_KEY)
        try:
            data = s.loads(token)

        except SignatureExpired:
            return {'error': 'Your token is expired, Please log in again!'}

        except BadSignature:
            return {'error': 'Invalid token, Please log in again!'}

        user = User.query.get(data['id'])

        return user

    def __repr__(self):
        return '<User: {}>'.format(self.fullname)


class BucketList(db.Model, AddUpdateDelete):
    """ buckets table"""

    __tablename__ = "bucketlist"

    bucket_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    bucket_name = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, server_default=func.now())
    date_modified = db.Column(db.DateTime, onupdate=func.now())
    bucket_items = db.relationship('BucketItems', backref='bucketlist', cascade='all, delete', lazy='dynamic')
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    def __repr__(self):
        return '<BucketList: {}'.format(self.bucket_name)


class BucketItems(db.Model, AddUpdateDelete):
    """ bucket items table"""

    __tablename__ = 'bucket_items'

    item_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    item_name = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, server_default=func.now())
    date_modified = db.Column(db.DateTime, onupdate=func.now())
    status = db.Column(db.Boolean, default=False, nullable=False)
    bucket_list_id = db.Column(db.Integer, db.ForeignKey('bucketlist.bucket_id'), nullable=False)

    def __repr__(self):
        return '<BucketItems: {}'.format(self.item_name)


class UserSchema(marshmallow.Schema):
    user_id = fields.Integer(dump_only=True)
    fullname = fields.String(validate=validate.Length(min=3))
    username = fields.String(required=True, validate=validate.Length(3, error='Field cannot be blank'))
    date_created = fields.DateTime()


class BucketListsSchema(marshmallow.Schema):
    bucket_id = fields.Integer(dump_only=True)
    bucket_name = fields.String(required=True, validate=validate.Length(min=3))
    bucket_items = fields.Nested('BucketItemsSchema', dump_only=True, many=True)
    created_by = fields.Integer(dump_only=True)
    date_created = fields.DateTime(dump_only=True)
    date_modified = fields.DateTime(dump_only=True)


class BucketItemsSchema(marshmallow.Schema):
    item_id = fields.Integer(dump_only=True)
    item_name = fields.String(validate=validate.Length(min=1))
    status = fields.Boolean(default=False)
    date_created = fields.DateTime()
    date_modified = fields.DateTime()
