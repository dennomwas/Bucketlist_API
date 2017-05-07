from flask import Blueprint, request, jsonify, json, g
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError


from models import db, auth, tokenization, User, UserSchema

auth_blueprint = Blueprint('auth_blueprint', __name__)
user_schema = UserSchema()
auth_api = Api(auth_blueprint)



class RegisterResource(Resource):
    def post(self):

        new_user = request.get_json()

        if not new_user:
            return {'error': 'No input provided'}, 400

        validate_user_errors = user_schema.validate(new_user)
        if validate_user_errors:
            return {'error': 'Check your fields and try again!'}, 400

        username = new_user.get('username')
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return {'error': ' username already exists!'}, 409

        try:
            user = User(fullname=new_user['fullname'],
                        username=new_user['username'],
                        password=new_user['password'])

            db.session.add(user)
            db.session.commit()

            return {'message': username + ' successfully registered'}, 201

        except Exception as error:

            db.session.rollback()
            return {'error': username + ' not registered, check your details and try again!'}



auth_api.add_resource(RegisterResource, '/register/')
auth_api.add_resource(RegisteredUsersResource, '/users')
auth_api.add_resource(LoginResource, '/login/')
