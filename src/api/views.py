from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Source, SourceColumnConfig, Graph, GraphDataset
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

def success_response(data, status, message=None):
    """
    Constructs a successful JSON response body.

    Arguments:
    - data (context dependant): Payload for the response data.
    - status (int): HTTP response code.
    - message (str, optional): Optional success message.
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

def error_response_graph_not_found(graph_id):
    """
    Constructs an error response that indicates that the specified graph does
    not exist.
    """
    return error_response(f'Graph `{graph_id}` does not exist.', 404)

def error_response_graph_dataset_not_found(dataset_id):
    """
    Constructs an error response that indicates that the specified graph dataset
    does not exist.
    """
    return error_response(f'Graph dataset `{dataset_id}` does not exist.', 404)

def read_source_at(location):
    """
    Reads a CSV source at the given location and returns the raw CSV data.

    Returns:
    This function returns a tuple of two values:
    1. Success state: If this is false, the 2nd tuple value will be a JSON error
       response that should be returned immediately.
    2. Response: This will be either a JSON error response (if the first tuple
       value is false), or the CSV file.
    """
    # Parse the URL for the source:
    try:
        url = urlparse(location)
    except URLError:
        return False, error_response(f'Cannot parse location: `{location}`.', 400)
    
    # Read the CSV data from the source:
    try:
        if url.scheme in ('http', 'https', 'ftp'):
            with urlopen(location) as response:
                csv_content = response.read().decode('utf-8')
        elif url.scheme == 'file':
            with open(url.path, 'r') as file:
                csv_content = file.read()
        else:
            return False, error_response(f'Cannot open location because `{url.scheme}` is not a supported URL scheme.', 400)
    except Exception as exception:
        return False, error_response(f'Failed to read CSV data from location `{location}`: {exception}.', 400)

    # Convert the CSV content into a CSV file:
    csv_file = StringIO(csv_content)

    return True, csv_file

@login_required
def source_list(request):
    """
    RESTful API endpoint for interacting with many sources.

    The main use of this endpoint is to either get a list of each of the
    sources, or to create a new source.

    Supported HTTP methods:
    - GET: Gets a list of every source.
    - POST: Creates a new source.
    """
    if request.method == 'GET':
        """
        The `GET` method retrieves a list of every source.
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
    elif request.method == 'POST':
        """
        The `POST` method will create a new source.
        """

        # Check permissions:
        if not request.user.has_perm('api.add_source'):
            return error_response_no_perms()
        
        # Get JSON request body:
        try:
            json_request = json.loads(request.body.decode('utf-8'))
        except:
            return error_response_invalid_json_body()
        
        name = json_request.get('name')
        if name is None:
            return error_response_expected_field('name')
        elif not isinstance(name, str):
            return error_response_invalid_field('name')
        location = json_request.get('location')
        if location is None:
            return error_response_expected_field('location')
        elif not isinstance(location, str):
            return error_response_invalid_field('location')
        has_header = json_request.get('has_header')
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
    else:
        return error_response_http_method_unsupported(request.method)

@login_required
def source_detail(request, source_id):
    """
    RESTful API endpoint for interacting with a single source.
    """

    if request.method == 'GET':
        """
        The `GET` method will fetch a single source.

        If the resource is not found, a 404 response code is returned.

        The user must have permission to view the corresponding model to
        interact with this API endpoint.
        """

        # Check permissions:
        if not request.user.has_perm('api.view_source'):
            return error_response_no_perms()

        source = Source.objects.get(id=source_id)
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
        if not request.user.has_perm('api.delete_source'):
            return error_response_no_perms()
        
        # Get the source:
        source = Source.objects.get(id=source_id)
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
        if not request.user.has_perm('api.change_source'):
            return error_response_no_perms()
        
        # Get JSON request body:
        try:
            json_request = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return error_response_invalid_json_body()

        # Get JSON fields:
        name = json_request.get('name')
        if name is None:
            return error_response_expected_field('name')
        elif not isinstance(name, str):
            return error_response_invalid_field('name')
        location = json_request.get('location')
        if name is None:
            return error_response_expected_field('location')
        elif not isinstance(name, str):
            return error_response_invalid_field('location')
        has_header = json_request.get('has_header')
        if has_header is None:
            return error_response_expected_field('has_header')
        elif not isinstance(has_header, bool):
            return error_response_invalid_field('has_header')

        # Get the source:
        source = Source.objects.get(id=source_id)
        if source is not None:
            # The source exists, we can now modify it:
            source.name = name.strip()
            source.location = location.strip()
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
        if not request.user.has_perm('api.view_source'):
            return error_response_no_perms()

        # Get the source:
        source = Source.objects.get(id=source_id)
        if source is None:
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
        
        # TODO: Should we translate the CSV data here?
        
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
    """
    RESTful API endpoint for interacting with many graphs.

    The main use of this endpoint is to either get a list of each of the graphs
    that exist with some information about the graph, or to create a new graph.

    Supported HTTP methods:
    - GET: Gets a list of every graph.
    - POST: Creates a new graph.
    """
    if request.method == 'GET':
        """
        The `GET` method retrieves a list of every graph.
        """

        # Check permissions:
        if not request.user.has_perm('api.view_graph'):
            return error_response_no_perms()
        
        # Get the graphs:
        graphs = Graph.objects.all()

        # Create a JSON array to write each graph to:
        graph_json = []

        # Add each graph to the graph JSON data:
        for graph in graphs:
            graph_json.append({
                'id': graph.id,
                'name': graph.name,
                'description': graph.description,
            })
        
        # Return the graph JSON data:
        return success_response(graph_json, 200)
    elif request.method == 'POST':
        """
        The `POST` method will create a new graph.
        """
        
        # Check permissions:
        if not request.user.has_perm('api.add_graph'):
            return error_response_no_perms()
        
        # Get JSON request body:
        try:
            json_request = json.loads(request.body.decode('utf-8'))
        except:
            return error_response_invalid_json_body()
        
        # Get and validate JSON fields:
        name = json_request.get('name')
        if name is None:
            return error_response_expected_field('name')
        elif not isinstance(name, str):
            return error_response_invalid_field('name')
        description = json_request.get('description')
        if description is None:
            return error_response_expected_field('description')
        elif not isinstance(description, str):
            return error_response_invalid_field('description')
        
        # Create the graph:
        try:
            graph_instance = Graph(name=name.strip(), description=description.strip())
            graph_instance.save()
        except ValidationError:
            return error_response('Failed to validate graph data.', 400)
        except Exception:
            return error_response('Failed to create graph.', 500)
        
        # Return success response:
        return success_response(None, 200, message='The graph was created successfully.')
    else:
        response_data = {
            'result': 'error',
            'message': f'Unknown HTTP method: `{request.method}`.'
        }
        return JsonResponse(response_data, status=405)

@login_required
def graph_detail(request, graph_id):
    """
    RESTful API endpoint for interacting with a single graph.
    """

    if request.method == 'GET':
        """
        The `GET` method will fetch data for a single graph.
        """
        
        # Check permissions:
        if not request.user.has_perm('api.view_graph'):
            return error_response_no_perms()
        
        # Get and return the graph:
        graph = Graph.objects.get(id=graph_id)
        if graph is not None:
            return success_response({ 'name': graph.name, 'description': graph.description }, 200)
        else:
            return error_response_graph_not_found(graph_id)
    elif request.method == 'DELETE':
        """
        The `DELETE` method will delete a single graph.
        """

        # Check permissions:
        if not request.user.has_perm('api.delete_graph'):
            return error_response_no_perms()
        
        # Get the graph:
        graph = Graph.objects.get(id=graph_id)
        if graph is not None:
            # The graph exists, delete the graph:
            graph.delete()
            return success_response(f'Deleted graph `{graph_id}`.', 200)
        else:
            return error_response_graph_not_found(graph_id)
    elif request.method == 'PUT':
        """
        The `PUT` method updates an entire graph.
        """

        # Check permissions:
        if not request.user.has_perm('api.change_graph'):
            return error_response_no_perms()
        
        # Get JSON request body:
        try:
            json_request = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return error_response_invalid_json_body()
        
        # Get JSON fields:
        name = json_request.get('name')
        if name is None:
            return error_response_expected_field('name')
        elif not isinstance(name, str):
            return error_response_invalid_field('name')
        description = json_request.get('description')
        if description is None:
            return error_response_expected_field('description')
        elif not isinstance(description, str):
            return error_response_invalid_field('description')
        
        # Get the graph that needs editing:
        graph = Graph.objects.get(id=graph_id)
        if graph is not None:
            graph.name = name.strip()
            graph.description = description.strip()
            graph.save()
            return success_response(None, 200, message=f'Updated graph `{graph_id}`.')
        else:
            return error_response_graph_not_found()
    else:
        return error_response_http_method_unsupported(request.method)

@login_required
def graph_dataset_list(request, graph_id):
    """
    RESTful API endpoint for interacting with the datasets that belong to a
    graph.
    """

    if request.method == 'GET':
        """
        The `GET` method is used to get every dataset that belongs to a graph.
        """

        # Check permissions:
        if not request.user.has_perm('view_graphdataset'):
            return error_response_no_perms()
        
        # Get the datasets that belong to the graph:
        datasets = GraphDataset.objects.filter(graph=graph_id)

        # Create a JSON array to write each dataset into:
        datasets_json = []

        # Iterate each dataset:
        for dataset in datasets:
            datasets_json.append({
                'id': dataset.id,
                'label': dataset.label,
                'plot_type': dataset.plot_type,
                'is_axis': dataset.is_axis,
                'source_name': dataset.source.name,
                'source_id': dataset.source.id,
                'column_id': dataset.column
            })
        
        # Construct and return the response data:
        return success_response(datasets_json, 200)
    elif request.method == 'POST':
        """
        The `POST` method is used to create a new dataset for a graph.
        """

        # Check permissions:
        if not request.user.has_perm('add_graphdataset'):
            return error_response_no_perms()
        
        # Get JSON request body:
        try:
            json_request = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return error_response_invalid_json_body()
        
        # Get JSON fields:
        label = json_request.get('label')
        if label is None:
            return error_response_expected_field('label')
        elif not isinstance(label, str):
            return error_response_invalid_field('label')
        plot_type = json_request.get('plot_type')
        if plot_type is None:
            return error_response_expected_field('plot_type')
        elif not isinstance(plot_type, str):
            return error_response_invalid_field('plot_type')
        is_axis = json_request.get('is_axis')
        if is_axis is None:
            return error_response_expected_field('is_axis')
        elif not isinstance(is_axis, bool):
            return error_response_invalid_field('is_axis')
        source_id = json_request.get('source_id')
        if source_id is None:
            return error_response_expected_field('source_id')
        elif not isinstance(source_id, int):
            return error_response_invalid_field('source_id')
        column_id = json_request.get('column_id')
        if column_id is None:
            return error_response_expected_field('column_id')
        elif not isinstance(column_id, int):
            return error_response_invalid_field('column_id')

        # Create the new dataset:
        try:
            dataset = GraphDataset(
                graph=Graph.objects.get(id=graph_id),
                plot_type=plot_type,
                label=label,
                is_axis=is_axis,
                source=Source.objects.get(id=source_id),
                column=column_id
            )
            dataset.save()
        except ValidationError:
            return error_response('Failed to validate dataset data.', 400)
        except Exception:
            return error_response('Failed to create dataset.', 500)
        return success_response('Created dataset.', 200)
    else:
        return error_response_http_method_unsupported(request.method)

@login_required
def graph_dataset_detail(request, graph_id, dataset_id):
    """
    RESTful API endpoint for interacting with a single datasets.
    """

    if request.method == 'GET':
        """
        The `GET` method is used to get information about a dataset that belongs
        to the specified graph.
        """

        # Check permissions:
        if not request.user.has_perm('view_graphdataset'):
            return error_response_no_perms()
        
        # Get the dataset:
        dataset = GraphDataset.objects.get(id=dataset_id, graph=graph_id)
        if dataset == None:
            return error_response_graph_dataset_not_found(dataset_id)
        else:
            response_data = {
                'label': dataset.label,
                'plot_type': dataset.plot_type,
                'is_axis': dataset.is_axis,
                'source_name': dataset.source.name,
                'source_id': dataset.source.id,
                'column_id': dataset.column
            }
            return success_response(response_data, 200)
    elif request.method == 'DELETE':
        """
        The `DELETE` method is used to delete a dataset from a graph.
        """

        # Check permissions:
        if not request.user.has_perm('delete_graphdataset'):
            return error_response_no_perms()
        
        # Delete the dataset:
        dataset = GraphDataset.objects.get(id=dataset_id, graph=graph_id)
        if dataset == None:
            return error_response_graph_dataset_not_found(dataset_id)
        else:
            dataset.delete()
            return success_response(f'Deleted dataset `${dataset_id}`.', 200)
    elif request.method == 'PUT':
        """
        The `PUT` method is used to update a dataset.
        """

        # Check permissions:
        if not request.user.has_perm('change_graphdataset'):
            return error_response_no_perms()
        
        # Get JSON request body:
        try:
            json_request = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return error_response_invalid_json_body()
        
        # Get JSON fields:
        label = json_request.get('label')
        if label is None:
            return error_response_expected_field('label')
        elif not isinstance(label, str):
            return error_response_invalid_field('label')
        plot_type = json_request.get('plot_type')
        if plot_type is None:
            return error_response_expected_field('plot_type')
        elif not isinstance(plot_type, str):
            return error_response_invalid_field('plot_type')
        is_axis = json_request.get('is_axis')
        if is_axis is None:
            return error_response_expected_field('is_axis')
        elif not isinstance(is_axis, bool):
            return error_response_invalid_field('is_axis')
        source_id = json_request.get('source_id')
        if source_id is None:
            return error_response_expected_field('source_id')
        elif not isinstance(source_id, int):
            return error_response_invalid_field('source_id')
        column_id = json_request.get('column_id')
        if column_id is None:
            return error_response_expected_field('column_id')
        elif not isinstance(column_id, int):
            return error_response_invalid_field('column_id')

        # Get the dataset:
        dataset = GraphDataset.objects.get(id=dataset_id, graph=graph_id)
        if dataset == None:
            return error_response_graph_dataset_not_found(dataset_id)
        else:
            dataset.label = label
            dataset.plot_type = plot_type
            dataset.is_axis = is_axis
            dataset.source = Source.objects.get(id=source_id)
            dataset.column = column_id
            dataset.save()
            return success_response(f'Updated dataset `{dataset_id}`.', 200)
    else:
        return error_response_http_method_unsupported(request.method)

@login_required
def graph_data(request, graph_id):
    """
    RESTful API endpoint for fetching graph data for ChartJs.
    """
    if request.method == 'GET':
        """
        The `GET` method is used to fetch ChartJs data for the graph.
        """

        # Check permissions:
        if not request.user.has_perm('view_graph'):
            return error_response_no_perms()
        
        # Get graph:
        try:
            graph = Graph.objects.get(id=graph_id)
        except ObjectDoesNotExist:
            return error_response_graph_not_found(graph_id)

        # Get datasets for the graph:
        datasets = GraphDataset.objects.filter(graph_id=graph_id)

        # Create ChartJS fields:
        data_json = {}
        datasets_json = []
        options_json = {
            'scales': {
                'x': {},
                'y': {}
            }
        }
        csv_files = {}

        # Populate the data with the datasets:
        if len(datasets) > 0:
            for dataset in datasets:
                if not dataset.is_axis and dataset.plot_type == 'none':
                    # The dataset should not be plotted.
                    pass
                else:
                    # The dataset should be plotted, we should read the dataset
                    # CSV values:
                    csv_file = csv_files.get(dataset.source.location)
                    if csv_file is None:
                        csv_read_result = read_source_at(dataset.source.location)
                        if not csv_read_result[0]:
                            # The read failed, this is an error response; we should
                            # return the error response:
                            return csv_read_result[1]
                        csv_file = csv_read_result[1]
                        csv_files[dataset.source.location] = csv_file
                    else:
                        csv_file.seek(0)
                    csv_reader = csv.reader(csv_file)

                    # If the source has a header, we should skip it:
                    if dataset.source.has_header:
                        next(csv_reader, None)
                    # We should get the current row:
                    current_row = next(csv_reader, None)
                    if current_row is None:
                        # There is no data to plot, we should skip this iteration:
                        continue
                    
                    # We should check that the columns value is in bounds:
                    column_id = dataset.column
                    if not (0 <= column_id < len(current_row)):
                        return error_response(f'Column is out of bounds (value: `{column_id}`, min: `0`, max: `{len(current_row)}`). Please update the column within the graph dataset to point to an existing column.', 400)
                    
                    # We should read the dataset data:
                    dataset_data = []
                    while current_row is not None:
                        if column_id < len(current_row):
                            dataset_data.append(current_row[column_id])
                        else:
                            dataset_data.append(None)
                        current_row = next(csv_reader, None)

                    # Determine if the dataset represents an axis or a plot:
                    if dataset.is_axis:
                        # The dataset represents an axis:
                        data_json['labels'] = dataset_data
                        options_json['scales']['x'] = {
                            'title': {
                                'display': True,
                                'text': dataset.label
                            }
                        }
                    else:
                        # The dataset needs plotting:
                        # TODO: Add CSV data translation here
                        
                        # Construct the dataset JSON object:
                        datasets_json.append({
                            'type': dataset.plot_type,
                            'label': dataset.label if dataset.label is not None else f'Dataset {dataset.id}',
                            'data': dataset_data
                        })

        # Assign the datasets:
        data_json['datasets'] = datasets_json

        # Return the ChartJS data:
        return success_response({
            'data': data_json,
            'options': options_json,
        }, 200)
    else:
        return error_response_http_method_unsupported(request.method)