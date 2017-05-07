import unittest
from flask import json
from bucket_api.models import db
# from bucket_api.app import create_app
from bucket_api.config import app_config
from bucket_api.models import User, BucketList, BucketItems


class BucketTest(unittest.TestCase):
    def setUp(self):
        self.app = app_config('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # add a bucket
        self.new_bucket = {
            'item_id': 1,
            'item_name': 'Camping',
            'date_created': '2016-08-12 11:57:23',
            'date_modified': '2017-08-12 11:57:23',
            'created_by': 'False'
        }

        # add a bucket item
        self.new_item = {
            'item_id': 1,
            'item_name': 'Camping',
            'date_created': '2016-08-12 11:57:23',
            'date_modified': '2017-08-12 11:57:23',
            'status': 'False'
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_a_new_bucket(self):

        response = self.client.post('/bucketlists/',
                                    data=json.dumps(self.new_bucket))

        self.assertEqual(response.status_code, 201)

    def test_create_a_new_item(self):

        response = self.client.post('/bucketlists/',
                                    data=json.dumps(self.new_item))

        self.assertEqual(response.status_code, 201)

    def test_update_item(self):
        new_update = {
            'item_id': 1,
            'item_name': 'Learn to Swim'

        }
        response = self.client.put('/bucketlists/1',
                                   data=json.dumps(new_update))

        self.assertEqual(response.status_code, 201)

    def test_view_all_items(self):
        response = self.client.get('/bucketlists/')

        self.assertEqual(response.status_code, 200)

    def test_delete_item(self):
        response = self.client.delete('/bucketlists/10')

        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()