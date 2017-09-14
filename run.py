#!/usr/bin/env python
import redis
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_socketio import SocketIO

from bucket_api import db, create_app
from bucket_api.models import User

app = create_app('development')

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
socketio = SocketIO(app,  message_queue='redis://localhost:6379')


def make_shell_context():
    return dict(app=app, db=db, User=User)


manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    socketio.run(app)
