import unittest
from flask import json, url_for
from bucket_api.models import db
from bucket_api import create_app
from bucket_api.models import User, BucketList, BucketItems


class BaseTests(unittest.TestCase):
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

        # add a bucket
        self.new_bucket = {
            'bucket_id': 1,
            'bucket_name': 'Camping',
            'date_created': '2016-08-12 11:57:23',
            'date_modified': '2017-08-12 11:57:23',
            'created_by': '1'
        }

        # update a bucket list
        self.new_update = {
            'bucket_id': 1,
            'bucket_name': 'Go to Nairobi',
            'date_modified': '2017-08-12 11:57:23',
        }

        # add a bucket item
        self.new_item = {
            'item_id': 1,
            'item_name': 'Camping',
            'date_created': '2016-08-12 11:57:23',
            'date_modified': '2017-08-12 11:57:23',
            'status': 'False'
        }

        self.search_name = {
            'name': 'camping'
        }
        # Update a bucket item
        self.new_update2 = {
            'item_id': 1,
            'item_name': 'Learn to Swim'

        }

    def headers(self):
        api_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        return api_headers


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

