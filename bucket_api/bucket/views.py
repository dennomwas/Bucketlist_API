from flask import Blueprint, request, json, make_response, g
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError
from flask_socketio import emit, send, join_room, leave_room

import datetime
from bucket_api import add_cors_headers
from bucket_api.models import (db, BucketList,
                               get_notifications,
                               BucketListsSchema,
                               BucketItems, BucketItemsSchema)
from bucket_api.pagination import ResourcePagination
from bucket_api.auth.views import AuthRequiredResource
from bucket_api.auth.views.LoginResource import connect_handler

bucket_blueprint = Blueprint('bucket_blueprint', __name__)
bucket_blueprint.after_request(add_cors_headers)

bucket_list_schema = BucketListsSchema(many=True)
single_bucket_list_schema = BucketListsSchema()
bucket_items_schema = BucketItemsSchema()
bucket_api = Api(bucket_blueprint)


def get_notification(self):
    emit('response', get_notifications,
         room=connect_handler,
         namespace='/notifications')


class BucketListResource(AuthRequiredResource):

    def post(self):

        # get user input
        new_bucket = request.get_json()

        # validate errors in the input
        if not new_bucket:
            return {'error': 'Input data not provided'}

        validate_bucket_errors = single_bucket_list_schema.validate(new_bucket)
        if validate_bucket_errors:
            return {'error': 'Check your fields and try again'}, 400

        bucket_name = new_bucket.get('bucket_name')
        existing_bucket = BucketList.query.filter_by(
            bucket_name=bucket_name).first()

        if existing_bucket:
            return {'error': 'Bucket list already exists'}, 409

        # persist data to the database
        try:
            new_bucket = BucketList()
            new_bucket.bucket_name = bucket_name
            new_bucket.created_by = g.user.user_id

            db.session.add(new_bucket)
            db.session.commit()

            return {'message': 'bucket added successfully'}, 201

        except SQLAlchemyError as error:
            print(error)
            db.session.rollback()
            return {'error': '{} not added, check your details and try again!'
                    .format(bucket_name)}, 400

    def get(self):

        # get the item name to search
        search_name = request.args.get('q', None, type=str)

        # search and display the buckets found
        if search_name:

            search_results = BucketList.query.filter_by(
                created_by=g.user.user_id).filter(
                BucketList.bucket_name.ilike('%' + search_name + '%'))

            if not search_results.count():
                return {'error': 'No results found'}, 404

            return bucket_list_schema.dump(search_results)

        else:

            # display all items
            resource_pagination = ResourcePagination(request,
                                                     query=BucketList.query.filter_by(
                                                         created_by=g.user.user_id),
                                                     resource_for_url='bucket_blueprint.all_bucketlists',
                                                     key_name='Results',
                                                     schema=bucket_list_schema)

            bucket_results = resource_pagination.paginate_buckets()
            return bucket_results


class BucketResource(AuthRequiredResource):

    def get(self, id):

        try:
            # get item from database by id
            one_bucket = BucketList.query.get(id)

            if not one_bucket:
                return {'error': 'The Bucket does not exist'}, 404

            # display the item found
            one_bucket = single_bucket_list_schema.dump(one_bucket).data
            return one_bucket

        except SQLAlchemyError as e:
            return {'error': 'Check your details and try again!'}

    def delete(self, id):
        try:
            # get item from database by id
            bucket = BucketList.query.get(id)

            if not bucket:
                return {'error': 'The Bucket does not exist'}, 404

            # delete the item found
            bucket.delete(bucket)

            return {'message': '{} successfully deleted'.format(bucket)}, 200

        except:
            db.session.rollback()
            return {'error': 'Unable to Delete'}, 200

    def put(self, id):

        # get item from database by id
        bucket = BucketList.query.get(id)

        if not bucket:
            return {'error': 'Requested Bucket does not exist'}, 404

        # get update information from user
        bucket_update = request.get_json(force=True)

        # validate user input
        if not bucket_update:
            return {'error': 'Invalid input!'}

        validate_errors = single_bucket_list_schema.validate(bucket_update)

        if validate_errors:
            return {'errors': 'Check your input data and try again!'}, 400

        try:
            # update new information
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

        # get input from the user
        new_item = request.get_json()

        # validate user input
        if not new_item:
            return {'error': 'Input data not provided'}

        validate_errors = bucket_items_schema.validate(new_item)
        if validate_errors:
            print(validate_errors)
            return {'error': 'Check your fields and try again'}

        item_name = new_item.get('item_name')
        existing_item = BucketItems.query.filter_by(
            item_name=item_name).first()

        if existing_item:
            return {'error': 'Item already exists'}, 409
        try:
            # post the new item to db
            new_item = BucketItems()
            new_item.item_name = item_name
            new_item.bucket_list_id = id

            db.session.add(new_item)
            db.session.commit()
            return {'message': '{} saved successfully'.format(item_name)}, 201

        except Exception as error:
            db.session.rollback()
            return {'message': '{} not saved, Please try again!'.format(item_name)}, 400

    def get(self, id):
        # gets all items from the database
        try:

            bucket_items = BucketItems.query.filter_by(bucket_list_id=id)

            if not bucket_items.count():
                return {'error': 'There are no Items to display'}, 404

            response_items = bucket_items_schema.dump(bucket_items, many=True)
            return response_items

        except Exception as e:
            return {'error': 'Check details and try again!'}, 400


class ItemsResource(AuthRequiredResource):

    def get(self, id, item_id):
        # gets one item from the database

        try:
            if item_id:
                single_item = BucketItems.query.get(item_id)

                if not single_item:
                    return {'error': 'Item not found'}, 404

                single_item = bucket_items_schema.dump(single_item)
                return single_item

        except Exception as e:
            return {'error': 'Check details and try again!'}, 400

    def delete(self, id, item_id):
        # deletes a single item from the database

        try:
            item = BucketItems.query.get(item_id)

            if not item:
                return {'error': 'The item does not exist'}, 404

            item.delete(item)
            return {'message': ' Item deleted successfully'}, 200

        except Exception as error:
            db.session.rollback()
            return {'error': 'Unable to delete Item'}, 400

    def put(self, id, item_id):
        # updates a single item in the database
        # get the item to update
        item_to_update = BucketItems.query.get(item_id)

        # validate the errors
        if not item_to_update:
            return {'error': 'Item not found'}, 404

        item_update = request.get_json(force=True)

        if not item_update:
            return {'error': 'Invalid input!'}, 400

        validate_errors = bucket_items_schema.validate(item_update)

        if validate_errors:
            return {'error': 'Check your details and try again!'}, 400

        try:
            # update the item

            if 'item_name' in item_update:
                item_to_update.item_name = item_update.get('item_name')
                item_to_update.date_modified = datetime.datetime.now()

            if 'status' in item_update:
                item_to_update.status = item_update.get('status')
                item_to_update.date_modified = datetime.datetime.now()

            # persist the update to the database
            item_to_update.update()
            return {"message": "successfully updated!"}, 200

        except Exception as error:
            db.session.rollback()
            return {'error': 'Item not updated!'}, 400


bucket_api.add_resource(BucketListResource, '/', endpoint='all_bucketlists')
bucket_api.add_resource(BucketResource, '/<int:id>/',
                        endpoint='one_bucketlist')
bucket_api.add_resource(BucketItemsResource,
                        '/<int:id>/items/', endpoint='all_bucketitems')
bucket_api.add_resource(
    ItemsResource, '/<int:id>/items/<int:item_id>/', endpoint='one_bucketitem')
