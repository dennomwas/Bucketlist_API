#!/usr/bin/env python
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from bucket_api.models import db, User
from bucket_api.config import app_config
from bucket_api.app import create_app


app = create_app(app_config['development'])

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

def make_shell_context():
    return dict(app=app, db=db, User=User)
manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
