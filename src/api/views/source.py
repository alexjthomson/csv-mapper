from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.core.exceptions import ValidationError, ObjectDoesNotExist

from api.models import Source
from api.views.response import *
from api.views.utility import clean_csv_value, decode_json_body, read_source_at

import csv
from json import JSONDecodeError

class SourceListView(APIView):
    """
    RESTful API endpoint for interacting with many sources.

    The main use of this endpoint is to either get a list of each of the
    sources, or to create a new source.
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Retrieves a list of every source.
        """

        # Check permissions:
        if not request.user.has_perm('api.view_source'):
            return error_response_no_perms()

        # Get the sources:
        sources = Source.objects.all()

        # Create a JSON array to write each source into:
        sources_json = []

        # Iterate each source:
        for source in sources:
            # Create the JSON entry and insert into the JSON sources array:
            source_data = {
                'id': source.id,
                'name': source.name,
                'location': source.location,
                'has_header': source.has_header
            }
            sources_json.append(source_data)

        # Construct and return the response data:
        return success_response(sources_json, 200)
    
    def post(self, request):
        """
        Creates a new source.
        """

        # Check permissions:
        if not request.user.has_perm('api.add_source'):
            return error_response_no_perms()
        
        # Get JSON request body:
        try:
            json_request = decode_json_body(request)
        except JSONDecodeError:
            return error_response_invalid_json_body()
        
        name = json_request['name']
        if name is None:
            return error_response_expected_field('name')
        elif not isinstance(name, str):
            return error_response_invalid_field('name')
        location = json_request['location']
        if location is None:
            return error_response_expected_field('location')
        elif not isinstance(location, str):
            return error_response_invalid_field('location')
        has_header = json_request['has_header']
        if has_header is None:
            return error_response_expected_field('has_header')
        elif not isinstance(has_header, bool):
            return error_response_invalid_field('has_header')

        # Create the source:
        try:
            source_instance = Source(name=name.strip(), location=location.strip(), has_header=has_header)
            source_instance.save()
        except ValidationError:
            return error_response('Failed to validate source data.', 400)
        except Exception:
            return error_response('Failed to create source.', 500)

        # Return the success response:
        return success_response(None, 200, message='The source was created successfully.')

class SourceDetailView(APIView):
    """
    RESTful API endpoint for interacting with a single source.
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, source_id):
        """
        Fetches a single source.

        If the resource is not found, a 404 response code is returned.

        The user must have permission to view the corresponding model to
        interact with this API endpoint.
        """

        # Check permissions:
        if not request.user.has_perm('api.view_source'):
            return error_response_no_perms()
        
        # Get requested source:
        try:
            source = Source.objects.get(id=source_id)
        except ObjectDoesNotExist:
            return error_response_source_not_found(source_id)
        return success_response({ 'name': source.name, 'location': source.location, 'has_header': source.has_header }, 200)
    
    def delete(self, request, source_id):
        """
        Deletes a single source.

        If the resource is deleted successfully, a 200 response code is
        returned; otherwise, if the resource is not found, 404 is returned.

        The user must have permission to delete the corresponding model to
        interact with this API endpoint.
        """
        
        # Check permissions:
        if not request.user.has_perm('api.delete_source'):
            return error_response_no_perms()
        
        # Get the requested source:
        try:
            source = Source.objects.get(id=source_id)
        except ObjectDoesNotExist:
            return error_response_source_not_found(source_id)
        
        # Delete the source:
        source.delete()
        return success_response(None, 200, message=f'Deleted source `{source_id}`.')
    
    def put(self, request, source_id):
        """
        Updates an entire source. In simple terms, this will replace the source
        data at an index with new data.

        If the resource is modified successfully, a 200 response code is
        returned; otherwise, if the resource is not found, 404 is returned.

        The user must have permission to modify the corresponding model to
        interact with this API endpoint.
        """

        # Check permissions:
        if not request.user.has_perm('api.change_source'):
            return error_response_no_perms()
        
        # Get JSON request body:
        try:
            json_request = decode_json_body(request)
        except JSONDecodeError:
            return error_response_invalid_json_body()

        # Get JSON fields:
        name = json_request['name']
        if name is None:
            return error_response_expected_field('name')
        elif not isinstance(name, str):
            return error_response_invalid_field('name')
        location = json_request['location']
        if name is None:
            return error_response_expected_field('location')
        elif not isinstance(name, str):
            return error_response_invalid_field('location')
        has_header = json_request['has_header']
        if has_header is None:
            return error_response_expected_field('has_header')
        elif not isinstance(has_header, bool):
            return error_response_invalid_field('has_header')

        # Get the requested source:
        try:
            source = Source.objects.get(id=source_id)
        except ObjectDoesNotExist:
            return error_response_source_not_found(source_id)
        
        # Modify the source:
        source.name = name.strip()
        source.location = location.strip()
        source.has_header = has_header
        source.save()
        return success_response(None, 200, message=f'Updated source `{source_id}`.')

class SourceDataView(APIView):
    """
    This API end-point is used to fetch the actual data behind a CSV source.
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, source_id):
        # Check permissions:
        if not request.user.has_perm('api.view_source'):
            return error_response_no_perms()

        # Get the requested source:
        try:
            source = Source.objects.get(id=source_id)
        except ObjectDoesNotExist:
            return error_response_source_not_found(source_id)

        csv_read_result = read_source_at(source.location)
        if not csv_read_result[0]:
            # The read failed, this is an error response; we should return it:
            return csv_read_result[1]
        csv_reader = csv.reader(csv_read_result[1])

        # Get the first row of the CSV resource. This may correspond to the
        # header, or may be the first row of actual data. This is required to
        # find the number of columns in the CSV file and if this is the header,
        # it is used to get column names:
        current_row = next(csv_reader, None)

        # Get the number of columns, this is useful to know. We can also
        # validate that the CSV file has at least one column and is therefore
        # valid by checking if there are no columns:
        column_count = len(current_row)
        if column_count == 0:
            return error_response('CSV source has zero columns.', 406)

        # Construct `columns` with pre-populated headers:
        columns = [
            {
                'name': clean_csv_value(column) if source.has_header else None,
                'unit': None,
                'transform': None,
                'data': []
            }
            for column in (current_row if source.has_header else range(column_count))
        ]
        
        # Collect the CSV rows:
        if source.has_header:
            # We should make sure we move to the next row if there is a header
            # so that we are pointing at the first row of data:
            current_row = next(csv_reader, None)
        
        while current_row is not None:
            for index, entry in enumerate(current_row):
                columns[index]['data'].append(clean_csv_value(entry))
            current_row = next(csv_reader, None)
        
        # Return the CSV data as JSON:
        return success_response(columns, 200)