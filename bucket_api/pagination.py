from flask import url_for, current_app,request


class ResourcePagination():
    def __init__(self, request, query, resource_for_url, key_name, schema):
        self.request = request
        self.query = query
        self.resource_for_url = resource_for_url
        self.key_name = key_name
        self.schema = schema
        self.results_per_page = current_app.config['PAGINATION_PAGE_SIZE']
        self.page_name = current_app.config['PAGINATION_PAGE_ARGUMENT_NAME']

    def paginate_buckets(self):

        limit = request.args.get('limit', type=int)
        if limit:
            self.min_results_per_page = limit
        else:
            self.max_results_per_page = limit

        page_number = self.request.args.get(self.page_name, 1, type=int)
        paginated_objects = self.query.paginate(page_number, per_page=self.results_per_page, error_out=False)
        objects = paginated_objects.items

        if paginated_objects.has_prev:
            previous_page = url_for(self.resource_for_url, page=page_number-1, _external=True)
        else:
            previous_page = None

        if paginated_objects.has_next:
            next_page = url_for(self.resource_for_url, page=page_number+1, _external=True)
        else:
            next_page = None

        dumped_objects = self.schema.dump(objects, many=True).data
        print(dumped_objects)
        return ({self.key_name: dumped_objects,
                 'previous': previous_page,
                 'next': next_page,
                 'count': paginated_objects.total
                 })
