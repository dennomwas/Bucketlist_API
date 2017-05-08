from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from bucket_api.config import app_config

db = SQLAlchemy()


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(app_config[config_filename])

    db.init_app(app)

    from bucket_api.auth.views import auth_blueprint
    from bucket_api.bucket.views import bucket_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(bucket_blueprint, url_prefix='/bucketlists')

    return app
