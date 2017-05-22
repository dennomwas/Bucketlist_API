from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from bucket_api.config import app_config
from bucket_api.models import db


def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers

    return response

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(app_config[config_filename])

    from . import models
    db.init_app(app)

    from bucket_api.auth.views import auth_blueprint
    from bucket_api.bucket.views import bucket_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(bucket_blueprint, url_prefix='/bucketlists')

    return app
