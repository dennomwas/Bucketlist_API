import datetime
from flask import Blueprint, request, json, make_response, g
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError
# import status

from models import db, User, BucketList, BucketListsSchema, BucketItems, BucketItemsSchema
from pagination import ResourcePagination
from auth.views import AuthRequiredResource


bucket_blueprint = Blueprint('bucket_blueprint', __name__)
bucket_list_schema = BucketListsSchema()
bucket_items_schema = BucketItemsSchema()
bucket_api = Api(bucket_blueprint)


bucket_api.add_resource(BucketListResource, '/', endpoint='all_bucketlists')
bucket_api.add_resource(BucketResource, '/<int:id>', endpoint='one_bucketlist')
bucket_api.add_resource(BucketItemsResource, '/<int:id>/items/', endpoint='all_bucketitems')
bucket_api.add_resource(ItemsResource, '/<int:bucket_id>/items/<int:item_id>', endpoint='one_bucketitem')

