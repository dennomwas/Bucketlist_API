import unittest
from flask import json, url_for
from bucket_api.models import db
from bucket_api import create_app
from bucket_api.models import User, BucketList, BucketItems


class AuthTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # User registration
        self.user = {
            'fullname': 'John Snow',
            'username': 'john_snow@gmail.com',
            'password': 'strong1'
        }

        # User login
        self.login = {
            'username': 'john_snow@gmail.com',
            'password': 'strong1'
        }

        # Login no username
        self.login_no_username = {
            'username': '',
            'password': 'strong1'
        }

        # Login no password
        self.login_no_password = {
            'username': 'john_snow@gmail.com',
            'password': ' '
        }

        # Login no username and password
        self.login_no_credentials = {
            'username': '',
            'password': ''
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

