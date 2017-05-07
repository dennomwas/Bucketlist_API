from flask import Flask

from models import db


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    db.init_app(app)

    from auth.views import auth_blueprint
    from bucket.views import bucket_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(bucket_blueprint, url_prefix='/bucketlists')

    return app
