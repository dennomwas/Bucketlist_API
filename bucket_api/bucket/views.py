import datetime
from flask import Blueprint, request, json, make_response, g
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError
# import status

from bucket_api.models import db, User, BucketList, BucketListsSchema, BucketItems, BucketItemsSchema
from bucket_api.pagination import ResourcePagination
from bucket_api.auth.views import AuthRequiredResource


bucket_blueprint = Blueprint('bucket_blueprint', __name__)
bucket_list_schema = BucketListsSchema()
bucket_items_schema = BucketItemsSchema()
bucket_api = Api(bucket_blueprint)


class BucketListResource(AuthRequiredResource):

    def post(self):
        new_bucket = request.get_json()

        if not new_bucket:
            return {'error': 'Input data not provided'}

        validate_bucket_errors = bucket_list_schema.validate(new_bucket)
        if validate_bucket_errors:
            return {'error': 'Check your fields and try again'}, 400

        bucket_name = new_bucket.get('bucket_name')
        existing_bucket = BucketList.query.filter_by(bucket_name=bucket_name).first()

        if existing_bucket:
            return {'error': 'Bucket list already exists'}, 409

        try:
            new_bucket = BucketList()
            new_bucket.bucket_name = bucket_name
            new_bucket.created_by = g.user.user_id

            db.session.add(new_bucket)
            db.session.commit()

            return {'message': '{} added successfully'.format(bucket_name)}, 201

        except Exception as error:

            db.session.rollback()
            return {'error': '{} not added, check your details and try again!'.format(bucket_name)}, 400

    def get(self):

        q = request.args.get('q')

        if q:
            search_results = BucketList.query.filter_by(created_by=g.user.user_id).filter(BucketList.bucket_name.like('%' + q + '%')).all()
            return search_results

        else:
            resource_pagination = ResourcePagination(request,
                                                     query=BucketList.query,
                                                     resource_for_url='bucket_blueprint.all_bucketlists',
                                                     key_name='results',
                                                     schema=bucket_list_schema)
            bucket_results = resource_pagination.paginate_buckets()
            return bucket_results


class BucketResource(AuthRequiredResource):

    def get(self, id):

        q = request.args.get('q')

        if q:
            search_results = BucketList.query.filter_by(created_by=g.user.user_id).filter(BucketList.bucket_name.like('%' + q + '%')).all()
            return search_results

        else:
            resource_pagination = ResourcePagination(request,
                                                     query=BucketList.query,
                                                     resource_for_url='bucket_blueprint.all_bucketlists',
                                                     key_name='results',
                                                     schema=bucket_list_schema)
            bucket_results = resource_pagination.paginate_buckets()
            return bucket_results


    def delete(self, id):
        try:
            bucket = BucketList.query.get(id)

            if not bucket:
                return {'error': 'The Bucket does not exist'}, 404

            bucket.delete(bucket)

            return {'message': '{} successfully deleted'.format(bucket)}

        except:
            db.session.rollback()
            return {'error': 'Unable to Delete'}, 200

    def put(self, id):

        bucket = BucketList.query.get(id)

        if not bucket:
            return {'error': 'Requested Bucket does not exist'}, 404

        bucket_update = request.get_json(force=True)

        if not bucket_update:
            return {'error': 'Invalid input!'}

        validate_errors = bucket_list_schema.validate(bucket_update)

        if validate_errors:
            return {'errors': 'Check your input data and try again!'}, 400

        try:
            if 'bucket_name' in bucket_update:
                bucket.bucket_name = bucket_update.get('bucket_name')
                bucket.date_modified = datetime.datetime.now()

                bucket.update()
                return self.get(id)

        except Exception as error:
            db.session.rollback()
            return {'error': 'Could not update!'}


class BucketItemsResource(AuthRequiredResource):
    def post(self, id):
        new_item = request.get_json()

        if not new_item:
            return {'error': 'Input data not provided'}

        validate_errors = bucket_items_schema.validate(new_item)
        if validate_errors:
            return {'error': 'Check your fields and try again'}

        item_name = new_item.get('item_name')
        existing_item = BucketItems.query.filter_by(item_name=item_name).first()

        if existing_item:
            return {'error': 'Item already exists'}
        try:
            new_item = BucketItems(item_name=new_item['item_name'])

            db.session.add(new_item)
            db.session.commit()
            return {'message': '{} saved successfully'.format(item_name)}

        except Exception as error:
            db.session.rollback()
            return {'message': '{} not saved, Please try again!'.format(item_name)},

class ItemsResource(AuthRequiredResource):

    def get(self, bucket_id, item_id):
        try:
            all_items = BucketItems.query.all()

            if not all_items:
                return {'error': 'There are no Items to display'}, 200

            all_items = bucket_items_schema.dump(all_items, many=True)
            return all_items

        except SQLAlchemyError as e:
            return {'error': 'Check details and try again!'}

    def delete(self, bucket_id, item_id):
        try:
            item = BucketItems.query.get(item_id)

            if not item:
                return {'error': 'The item does not exist'}, 404

            item.delete(item)
            return {'message': ' Item deleted successfully'}

        except Exception as error:
            db.session.rollback()
            return {'error': 'Unable to delete Item'}, 200

    def put(self, bucket_id, item_id):

        item_to_update = BucketItems.query.get(item_id)

        if not item_to_update:
            return {'error': 'Item not found'}, 404

        item_update = request.get_json(force=True)

        if not item_update:
            return {'error': 'Invalid input!'},

        validate_errors = bucket_items_schema.validate(item_update)

        if validate_errors:
            return {'error': 'Check your details and try again!'}, 400

        try:
            if 'item_name' in item_update:
                item_to_update.item_name = item_update.get('item_name')
                item_to_update.date_modified = datetime.datetime.now()

            if 'status' in item_update:
                item_to_update.status = item_update.get('status')
                item_to_update.date_modified = datetime.datetime.now()


                item_to_update.update()
                return self.get(bucket_id, item_id)

        except SQLAlchemyError as error:
            db.session.rollback()
            return {'error': 'Item not updated!'}


# class BucketSearch(AuthRequiredResource):
#
#     def get(self, search_name):
#
#         if not search_name:
#             return {'error': 'Please Enter a name to search!'}
#
#         try:
#             search_results = BucketList.query.filter(BucketList.bucket_name.like('%' + search_name + '%')).all()
#
#             if not search_results:
#                 return {'message': 'No Buckets found!'}
#             return search_results
#
#         except SQLAlchemyError as e:
#             return {'error': 'Please try again later!'}


bucket_api.add_resource(BucketListResource, '/', endpoint='all_bucketlists')
bucket_api.add_resource(BucketResource, '/<int:id>', endpoint='one_bucketlist')
bucket_api.add_resource(BucketItemsResource, '/<int:id>/items/', endpoint='all_bucketitems')
bucket_api.add_resource(ItemsResource, '/<int:bucket_id>/items/<int:item_id>', endpoint='one_bucketitem')


"""
token authentication
search
pagination"""