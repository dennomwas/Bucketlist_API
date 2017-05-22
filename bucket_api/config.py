import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """ common configurations"""
    PORT = 5000
    HOST = "127.0.0.1"
    SECRET_KEY = "something_not_easy"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}: {DB_PASS}@{DB_ADDR}/{DB_NAME}"\
        .format(DB_USER="mwas", DB_PASS="", DB_ADDR="127.0.0.1", DB_NAME="bucketlist_db")


class DevelopmentConfig(Config):
    """ Development configurations"""

    DEBUG = True
    SQLALCHEMY_ECHO = True
    PAGINATION_PAGE_SIZE = 10
    PAGINATION_PAGE_ARGUMENT_NAME = 'page'


class ProductionConfig(Config):
    """ Production Configurations"""

    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """ Testing configurations"""
    SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}: {DB_PASS}@{DB_ADDR}/{DB_NAME}" \
        .format(DB_USER="mwas", DB_PASS="", DB_ADDR="127.0.0.1", DB_NAME="test_db")


app_config = {

    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# basedir = os.path.abspath(os.path.dirname(__file__))
# DEBUG = True
# PORT = 5000
# HOST = "127.0.0.1"
# SQLALCHEMY_ECHO = False
# SQLALCHEMY_TRACK_MODIFICATIONS = True
# SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}: {DB_PASS}@{DB_ADDR}/{DB_NAME}"\
#     .format(DB_USER="mwas", DB_PASS="", DB_ADDR="127.0.0.1", DB_NAME="bucketlist_db")
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
