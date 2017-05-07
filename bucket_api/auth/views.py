from flask import Blueprint, request, jsonify, json, g
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError


from bucket_api.models import db, auth, tokenization, User, UserSchema

auth_blueprint = Blueprint('auth_blueprint', __name__)
user_schema = UserSchema()
auth_api = Api(auth_blueprint)


@auth.verify_password
def verify_user_password(username, password):
    user = User.query.filter_by(username=username).first()

    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True

@tokenization.verify_token
def verify_token(token):

    user = User.verify_auth_token(token)

    if not user:
        return False

    g.user = user
    return True

class AuthRequiredResource(Resource):
    method_decorators = [tokenization.login_required]


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


class RegisteredUsersResource(AuthRequiredResource):
    def get(self, user_id):
        users = User.query.get(id)
        all_users = user_schema.dump(users).data
        return all_users

class LoginResource(Resource):
    def post(self):
        login_details = request.get_json()

        if not login_details:
            return {'error': 'No input provided'}, 400

        validate_user_errors = user_schema.validate(login_details)
        if validate_user_errors:
            return {'error': 'Check your fields and try again!'}, 400

        username = login_details.get('username')
        password = login_details.get('password')

        user_login = User.query.filter_by(username=username).first()

        if user_login and verify_user_password(username, password):

            token = user_login.generate_auth_token()

            user_login = user_schema.dump(user_login).data
            return {'user_login': user_login,
                    'token': token.decode('ascii')}, 201

        return {'error': 'Incorrect Username or Password'}, 400


auth_api.add_resource(RegisterResource, '/register/')
auth_api.add_resource(RegisteredUsersResource, '/users')
auth_api.add_resource(LoginResource, '/login/')
