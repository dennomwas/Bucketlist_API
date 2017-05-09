from flask import json
from bucket_api.tests.Basetest import AuthTest


class AuthTesting(AuthTest):

    def headers(self):
        api_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        return api_headers

    def create_user(self):
        new_user = self.client.post('/auth/register/',
                                    headers=self.headers(),
                                    data=json.dumps(self.user))
        return new_user

    def test_register_account(self):
        # register new user
        create_new_user = self.create_user()

        # Assert user has been created
        self.assertEqual(create_new_user.status_code, 201)

    def test_user_already_exist(self):
        # Create user 1
        registered_user1 = self.create_user()

        # Create user 2 with same credentials as user 1
        registered_user2 = self.create_user()

        # Assert conflict
        self.assertEqual(registered_user2.status_code, 409)

    def test_login(self):

        # Register the user
        create_user_response = self.create_user()

        # Login the user
        login_response = self.client.post('/auth/login/',
                                          headers=self.headers(),
                                          data=json.dumps(self.login))
        # assert successful login
        self.assertEqual(login_response.status_code, 201)

    def test_login_username_missing(self):
        # Register the user
        register_new_user = self.create_user()

        login_no_username = self.client.post('/auth/login/',
                                             headers=self.headers(),
                                             data=json.dumps(self.login_no_username))
        # Assert bad request
        self.assertEqual(login_no_username.status_code, 400)

    def test_login_password_missing(self):
        # Register the user
        register_new_user = self.create_user()

        login_no_password = self.client.post('/auth/login/',
                                             headers=self.headers(),
                                             data=json.dumps(self.login_no_password))
        # Assert bad request
        self.assertEqual(login_no_password.status_code, 400)

    def test_no_username_and_password(self):
        # Register the user
        register_new_user = self.create_user()

        login_no_credentials = self.client.post('/auth/login/',
                                                headers=self.login_no_credentials,
                                                data=json.dumps(self.login_no_credentials))
        # Assert bad request
        self.assertEqual(login_no_credentials.status_code, 400)


