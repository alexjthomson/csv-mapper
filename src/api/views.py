from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import GraphModel, SourceModel, SourceColumnConfigModel
import csv
import json
import asyncio
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.error import URLError
from io import StringIO

ALLOWED_CSV_CHARSET='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-./\\({)}[]+<>,!?£$%^&* '

def clean_csv_value(value):
    """
    Cleans a CSV entry.
    """
    return ''.join([char for char in value if char in ALLOWED_CSV_CHARSET]).strip()

def success_response(data, status, message=None, safe=True):
    """
    Constructs a successful JSON response body.

    Arguments:
    - data (context dependant): Payload for the response data.
    - status (int): HTTP response code.
    - message (str, optional): Optional success message.
    - safe: If set to False, any object can be passed for serialisation
      (otherwise only dict instances are allowed).
    """
    response_data = { 'result': 'success' }
    if message != None:
        response_data['message'] = message
    if data != None:
        response_data['data'] = data
    return JsonResponse(response_data, status=status)

def error_response(message, status):
    """
    Constructs an error JSON response body.

    Arguments:
    - message (str): Error message.
    - status (int): HTTP response code.
    """
    return JsonResponse({ 'result': 'error', 'message': message }, status=status)

def error_response_no_perms():
    """
    Constructs an error response that indicates the user does not have the
    correct permissions to perform an action.
    """
    return error_response('User does not have permission to perform this action.', 403)

def error_response_invalid_json_body():
    """
    Constructs an error response that indicates that the JSON response body sent
    by the client is invalid.
    """
    return error_response('Invalid JSON request body.', 400)

def error_response_expected_field(field_name):
    """
    Constructs an error response that indicates that a field was expected but
    was not found.
    """
    return error_response(f'Expected `{field_name}` field was not found.', 400)

def error_response_invalid_field(field_name):
    """
    Constructs an error response that indicates that a field is invalid and
    cannot be consumed by the API.
    """
    return error_response(f'Expected `{field_name}` field has an invalid value.', 400)

def error_response_http_method_unsupported(http_method):
    """
    Constructs an error response that indicates that the HTTP method used to
    access the API endpoint is not a supported method.
    """
    return error_response(f'Unsupported HTTP method: `{http_method}`.', 405)

def error_response_source_not_found(source_id):
    """
    Constructs an error response that indicates that the specified source does
    not exist.
    """
    return error_response(f'Source `{source_id}` does not exist.', 404)

@login_required
def source_list(request):
    """
    RESTful API endpoint for interacting with many sources.
    """
    if request.method == 'GET':
        """
        The `GET` method retrieves a list of every source.
        """

        # Check permissions:
        if not request.user.has_perm('api.view_sourcemodel'):
            return error_response_no_perms()

        # Get the sources:
        sources = SourceModel.objects.all()

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
        return success_response(sources_json, 200, safe=False)
    elif request.method == 'POST':
        """
        The `POST` method will create a new source.

        This expects a JSON body with `source_name` and `source_location`
        fields.
        """

        # Check permissions:
        if not request.user.has_perm('api.add_sourcemodel'):
            return error_response_no_perms()
        
        # Get JSON request body:
        try:
            json_request = json.loads(request.body.decode('utf-8'))
        except:
            return error_response_invalid_json_body()
        
        # Get and validate the `name`:
        name = json_request['name']
        if name is None:
            return error_response_expected_field('name')
        elif not isinstance(name, str):
            return error_response_invalid_field('name')
        
        # Get and validate the `location`:
        location = json_request['location']
        if location is None:
            return error_response_expected_field('location')
        elif not isinstance(location, str):
            return error_response_invalid_field('location')

        # Get and validate the `has_header`:
        has_header = json_request['has_header']
        if has_header is None:
            return error_response_expected_field('has_header')
        elif not isinstance(has_header, bool):
            return error_response_invalid_field('has_header')

        # Create the source:
        try:
            source_instance = SourceModel(name=name, location=location, has_header=has_header)
            source_instance.save()
        except ValidationError:
            return error_response('Failed to validate source data.', 400)
        except Exception:
            return error_response('Failed to create source.', 500)

        # Return the success response:
        return success_response(None, 200, message='The source was created successfully.')
    else:
        return error_response_http_method_unsupported(request.method)

@login_required
def source_detail(request, source_id):
    """
    RESTful API endpoint for interacting with a single source.

    This endpoint will perform different actions depending on the HTTP request
    method used to access the endpoint.
    """

    if request.method == 'GET':
        """
        The `GET` method will fetch a single source.

        If the resource is not found, a 404 response code is returned.

        The user must have permission to view the corresponding model to
        interact with this API endpoint.
        """

        # Check permissions:
        if not request.user.has_perm('api.view_sourcemodel'):
            return error_response_no_perms()

        source = SourceModel.objects.get(id=source_id)
        if source is not None:
            return success_response({ 'name': source.name, 'location': source.location, 'has_header': source.has_header }, 200)
        else:
            return error_response_source_not_found(source_id)
    elif request.method == 'DELETE':
        """
        The `DELETE` method will delete a single source.

        If the resource is deleted successfully, a 200 response code is
        returned; otherwise, if the resource is not found, 404 is returned.

        The user must have permission to delete the corresponding model to
        interact with this API endpoint.
        """
        
        # Check permissions:
        if not request.user.has_perm('api.delete_sourcemodel'):
            return error_response_no_perms()
        
        # Get the source:
        source = SourceModel.objects.get(id=source_id)
        if source is not None:
            # The source exists, we can now delete it:
            source.delete()
            return success_response(f'Deleted source `{source_id}`.', 200)
        else:
            return error_response_source_not_found(source_id)
    elif request.method == 'PUT':
        """
        The `PUT` method updates an entire source. In simple terms, this will
        replace the source data at an index with new data.

        If the resource is modified successfully, a 200 response code is
        returned; otherwise, if the resource is not found, 404 is returned.

        The user must have permission to modify the corresponding model to
        interact with this API endpoint.
        """

        # Check permissions:
        if not request.user.has_perm('api.change_sourcemodel'):
            return error_response_no_perms()
        
        # Get JSON request body:
        try:
            json_request = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
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

        # Get the source:
        source = SourceModel.objects.get(id=source_id)
        if source is not None:
            # The source exists, we can now modify it:
            source.name = name
            source.location = location
            source.has_header = has_header
            source.save()
            return success_response(None, 200, message=f'Updated source `{source_id}`.')
        else:
            return error_response_source_not_found(source_id)
    else:
        return error_response_http_method_unsupported(request.method)

@login_required
def source_data(request, source_id):
    """
    This API end-point is used to fetch the actual data behind a CSV source.
    """
    if request.method == 'GET':
        # Check permissions:
        if not request.user.has_perm('api.view_sourcemodel'):
            return error_response_no_perms()

        # Get the source:
        source = SourceModel.objects.get(id=source_id)
        if source is None:
            return error_response_source_not_found(source_id)

        # Parse the URL to the source:
        try:
            source_url = urlparse(source.location)
        except URLError:
            return error_response(f'Cannot parse location: `{source.location}`.', 400)
        
        # Read the CSV data from the source:
        try:
            if source_url.scheme in ('http', 'https', 'ftp'):
                with urlopen(source.location) as response:
                    csv_content = response.read().decode('utf-8')
            elif source_url.scheme == 'file':
                with open(source_url.path, 'r') as file:
                    csv_content = file.read()
            else:
                return error_response(f'Cannot open location because `{source_url.scheme}` is not a supported URL scheme.', 400)
        except Exception:
            return error_response(f'Failed to read CSV data from location: `{source.location}`.', 400)

        # Convert the CSV content into a CSV file:
        csv_file = StringIO(csv_content)
        csv_reader = csv.reader(csv_file)

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

        # Construct `columns`:
        columns = []
        # Pre-populate the header values:
        if source.has_header:
            for column in current_row:
                columns.append({
                    'name': clean_csv_value(column),
                    'unit': None,
                    'transform': None,
                    'data': []
                })
        else:
            for i in range(column_count):
                columns.append({
                    'name': None,
                    'unit': None,
                    'transform': None,
                    'data': []
                })
        # Check for column configuration overrides:
        column_configs = SourceColumnConfigModel.objects.filter(source_id=source_id)
        for config in column_configs:
            # TODO: Validate this does what it is expected to do
            columns[config.column_id] = {
                'name': clean_csv_value(config.column_name),
                'unit': config.unit,
                'transform': SourceColumnConfigModel.Transformers.from_str(config.transform_name),
                'data': []
            }
        
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
    else:
        return error_response_http_method_unsupported(request.method)

@login_required
def graph_list(request):
    # TODO
    if request.method == 'GET':
        response_data = {
            'result': 'error',
            'message': 'Not implemented.'
        }
        return JsonResponse(response_data, status=500)
    else:
        response_data = {
            'result': 'error',
            'message': f'Unknown HTTP method: `{request.method}`.'
        }
        return JsonResponse(response_data, status=405)

@login_required
def graph_detail(request):
    # TODO
    if request.method == 'GET':
        response_data = {
            'result': 'error',
            'message': 'Not implemented.'
        }
        return JsonResponse(response_data, status=500)
    else:
        response_data = {
            'result': 'error',
            'message': f'Unknown HTTP method: `{request.method}`.'
        }
        return JsonResponse(response_data, status=405)