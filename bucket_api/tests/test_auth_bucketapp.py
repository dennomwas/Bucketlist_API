import unittest
from flask import json, url_for
from bucket_api.models import db
# from bucket_api.app import create_app
from bucket_api.config import app_config
from bucket_api.models import User, BucketList, BucketItems


class AuthTest(unittest.TestCase):
    def setUp(self):
        self.app = app_config('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()


        # user registration
        self.user = {
            'fullname': 'John Snow',
            'username': 'john_snow@gmail.com',
            'password': 'strong1'
        }
        # user login
        self.login = {
            'username': 'john_snow@gmail.com',
            'password': 'strong1'
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_account(self):
        response = self.client.post('/auth/register',
                                    data=json.dumps(self.user))

        self.assertEqual(response.status_code, 201)

    def test_user_already_exist(self):

        user = {
            'fullname': 'John Snow',
            'username': 'john_snow@gmail.com',
            'password': 'strong1'
        }
        response = self.client.post('/auth/register',
                                    data=json.dumps(user))

        self.assertEqual(response.status_code, 409)
        self.assertTrue('Username already exists!' in json.load(response.data))

    def test_login(self):
        response = self.client.get('/auth/login',
                                   data=json.dumps(self.login))

        self.assertEqual(response.status_code, 202)

    def test_login_username_missing(self):
        self.login = {
            'username': ' ',
            'password': 'strong1'
        }
        response = self.client.get('/auth/login',
                                   data=json.dumps(self.login))

        self.assertEqual(response.status_code, 400)

    def test_login_password_missing(self):
        self.login = {
            'username': 'john_snow@gmail.com',
            'password': ' '
        }
        response = self.client.get('/auth/login',
                                   data=json.dumps(self.login))

        self.assertEqual(response.status_code, 400)

    def test_no_username_and_password(self):
        self.login = {
            'username': ' ',
            'password': ' '
        }
        response = self.client.get('/auth/login',
                                   data=json.dumps(self.login))

        self.assertEqual(response.status_code, 400)

    def test_logout(self):
        response = self.client.delete('/auth/logout')

        self.assertEqual(response.status_code, 200)


