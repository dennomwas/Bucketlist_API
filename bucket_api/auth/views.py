from flask import Blueprint, request, jsonify, json, g
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError


from models import db, auth, tokenization, User, UserSchema

auth_blueprint = Blueprint('auth_blueprint', __name__)
user_schema = UserSchema()
auth_api = Api(auth_blueprint)




auth_api.add_resource(RegisterResource, '/register/')
auth_api.add_resource(RegisteredUsersResource, '/users')
auth_api.add_resource(LoginResource, '/login/')




