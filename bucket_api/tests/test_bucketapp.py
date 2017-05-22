from flask import json
from bucket_api.tests.Basetest import BaseTests

#
class BucketTesting(BaseTests):
#
    def create_user(self):
        new_user = self.client.post('/auth/register/',
                                    headers=self.headers(),
                                    data=json.dumps(self.user))
        return new_user

    def login_user(self):
        user_login = self.client.post('auth/login/',
                                      headers=self.headers(),
                                      data=json.dumps(self.login))
        return user_login

    def create_new_bucket(self):
        # Create user
        test_user = self.create_user()

        # login user
        user = self.login_user()
        self.assertEqual(user.status_code, 201)

        # generate authentication credentials
        auth_header = self.headers()
        auth_header['Authorization'] = 'Bearer ' + json.loads(user.data.decode())['token']

        # Add a new bucket
        new_bucket = self.client.post('/bucketlists/',
                                      headers=auth_header,
                                      data=json.dumps(self.new_bucket))
        return new_bucket

    def create_new_item(self):
        # Create user
        test_user = self.create_user()

        # login user
        user = self.login_user()

        self.assertEqual(user.status_code, 201)

        # generate authentication credentials
        auth_header = self.headers()
        auth_header['Authorization'] = 'Bearer ' + json.loads(user.data.decode())['token']

        # add new bucket item
        new_item = self.client.post('/bucketlists/1/items/',
                                    headers=auth_header,
                                    data=json.dumps(self.new_item))
        return new_item

    def test_create_a_new_bucket(self):
        # create new bucket
        new_bucket = self.create_new_bucket()

        # assert bucket created
        self.assertEqual(new_bucket.status_code, 201)

    def test_create_duplicate_bucket(self):
        # create new bucket
        new_bucket1 = self.create_new_bucket()

        # create duplicate bucket
        new_bucket2 = self.create_new_bucket()

        # assert bucket created
        self.assertEqual(new_bucket2.status_code, 409)

    def test_update_bucket(self):
        # Create user
        test_user = self.create_user()

        # login user
        user = self.login_user()
        self.assertEqual(user.status_code, 201)

        # generate authentication credentials
        auth_header = self.headers()
        auth_header['Authorization'] = 'Bearer ' + json.loads(user.data.decode())['token']

        # create new bucket
        new_bucket = self.create_new_bucket()

        bucket_update = self.client.put('/bucketlists/1/',
                                        headers=auth_header,
                                        data=json.dumps(self.new_update))

        self.assertEqual(bucket_update.status_code, 200)

    def test_delete_bucket(self):
        # Create user
        test_user = self.create_user()

        # login user
        user = self.login_user()
        self.assertEqual(user.status_code, 201)

        # generate authentication credentials
        auth_header = self.headers()
        auth_header['Authorization'] = 'Bearer ' + json.loads(user.data.decode())['token']

        # create new bucket
        new_bucket = self.create_new_bucket()

        response = self.client.delete('/bucketlists/1/',
                                      headers=auth_header,
                                      data=json.dumps(self.new_bucket))

        self.assertEqual(response.status_code, 200)

    def test_create_a_new_item(self):
        # create new bucket
        new_bucket = self.create_new_bucket()

        # create new bucket item
        new_bucket_item = self.create_new_item()

        # assert bucket created
        self.assertEqual(new_bucket_item.status_code, 201)

    def test_bucket_does_not_exist(self):
        # Create user
        test_user = self.create_user()

        # login user
        user = self.login_user()
        self.assertEqual(user.status_code, 201)

        # generate authentication credentials
        auth_header = self.headers()
        auth_header['Authorization'] = 'Bearer ' + json.loads(user.data.decode())['token']

        # create new bucket
        new_bucket = self.create_new_bucket()

        response = self.client.get('/bucketlists/14/',
                                   headers=auth_header)

        self.assertEqual(response.status_code, 404)

    def test_update_item(self):
        # Create user
        test_user = self.create_user()

        # login user
        user = self.login_user()
        self.assertEqual(user.status_code, 201)

        # generate authentication credentials
        auth_header = self.headers()
        auth_header['Authorization'] = 'Bearer ' + json.loads(user.data.decode())['token']

        # create new bucket
        bucket = self.create_new_bucket()

        # create new item
        new_item_update = self.create_new_item()

        item_update = self.client.put('/bucketlists/1/items/1/',
                                        headers=auth_header,
                                        data=json.dumps(self.new_update))

        self.assertEqual(item_update.status_code, 200)

    def test_view_items(self):
        # Create user
        test_user = self.create_user()

        # login user
        user = self.login_user()
        self.assertEqual(user.status_code, 201)

        # generate authentication credentials
        auth_header = self.headers()
        auth_header['Authorization'] = 'Bearer ' + json.loads(user.data.decode())['token']

        # create new bucket
        new_bucket = self.create_new_bucket()

        response = self.client.get('/bucketlists/1/items/',
                                   headers=auth_header)
        # check no items
        self.assertEqual(response.status_code, 404)

    def test_item_does_not_exist(self):
        # Create user
        test_user = self.create_user()

        # login user
        user = self.login_user()
        self.assertEqual(user.status_code, 201)

        # generate authentication credentials
        auth_header = self.headers()
        auth_header['Authorization'] = 'Bearer ' + json.loads(user.data.decode())['token']

        # create new bucket
        new_bucket = self.create_new_bucket()

        response = self.client.get('/bucketlists/1/items/24/',
                                   headers=auth_header)

        self.assertEqual(response.status_code, 404)

    def test_delete_item(self):
        # Create user
        test_user = self.create_user()

        # login user
        user = self.login_user()
        self.assertEqual(user.status_code, 201)

        # generate authentication credentials
        auth_header = self.headers()
        auth_header['Authorization'] = 'Bearer ' + json.loads(user.data.decode())['token']

        # create new bucket
        bucket = self.create_new_bucket()

        # create new item
        new_item_update = self.create_new_item()

        response = self.client.delete('/bucketlists/1/items/1/',
                                      headers=auth_header)

        self.assertEqual(response.status_code, 200)
    #
