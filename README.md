[![Build Status](https://travis-ci.org/dennomwas/Bucketlist_API.svg?branch=master)](https://travis-ci.org/dennomwas/Bucketlist_API) [![Coverage Status](https://coveralls.io/repos/github/dennomwas/Bucketlist_API/badge.svg?branch=develop)](https://coveralls.io/github/dennomwas/Bucketlist_API?branch=develop)

# Bucketlist_API

### Introduction
This is an API built on flask restful to create and manage an individuals/group bucketlists 
It implements token Based Authentication for the API and the only methods available to unauthenticated users are register and login. 

### How to Setup
1. Clone the repository
``` diff 
-$ git@github.com:dennomwas/Bucketlist_API.git
```
2. Cd to the repository and create a virtual environment
```diff
-$ cd /Bucketlist_API

-$ virtualenv venv

-$ source venv/bin/activate
```
3. Pip install requirements
```diff
-$ (venv) pip install -r requirements.txt
```
4. To make Database migrations, run the following commands, to create a database for the app and initialize tables
``` diff
-$ python run.py db init

-$ python run.py db migrate

-$ python run.py db migrate
``` 
### Run the application
Run the following command in the terminal to launch the application
```dif
-$ python run.py runserver
```
### API Documentation
Access control mapping is as listed below.

Endpoints | Public access
------------ | -------------
POST /auth/login | TRUE
POST /auth/register | TRUE
POST /bucketlists/ | FALSE
GET /bucketlists/ | FALSE
GET /bucketlists/<id> | FALSE
PUT /bucketlists/<id> | FALSE
DELETE /bucketlists/<id> | FALSE
POST /bucketlists/<id>/items/ | FALSE
PUT /bucketlists/<id>/items/<item_id> | FALSE
DELETE /bucketlists/<id>/items/<item_id> | FALSE

### Built with
[Python flask restful](https://flask-restful.readthedocs.io/en/0.3.5/)  
[Postgres](https://www.postgresql.org/docs/manuals/)

### Acknowledgements
  * To all who gave me invaluable advice and guidance
  * Inspiration
  * Andela - Kenya  
##### Enjoy the application!
