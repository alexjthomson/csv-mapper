from django.core.exceptions import ValidationError
from django.core.serializers import serialize
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import DataSourceModel
import json

@login_required
def source_list(request):
    """
    RESTful API endpoint for interacting with many sources.
    """
    if request.method == 'GET':
        """
        The `GET` method retrieves a list of every source.
        """

        # Get the sources:
        sources = DataSourceModel.objects.all()

        # Create a JSON array to write each source into:
        sources_json = []

        # Iterate each source:
        for source in sources:
            # Create the JSON entry and insert into the JSON sources array:
            source_data = {
                'id': source.id,
                'name': source.name,
                'location': source.location
            }
            sources_json.append(source_data)

        # Construct and return the response data:
        response_data = {
            'result': 'success',
            'data': sources_json
        }
        return JsonResponse(response_data, safe=False, status=200)
    elif request.method == 'POST':
        """
        The `POST` method will create a new source.

        This expects a JSON body with `source_name` and `source_location`
        fields.
        """
        
        # Get the JSON body:
        try:
            request_data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            response_data = {
                'result': 'error',
                'message': 'Invalid JSON request body.'
            }
            return JsonResponse(response_data, status=400)
        except:
            response_data = {
                'result': 'error',
                'message': 'Failed to parse JSON request body.'
            }
            return JsonResponse(response_data, status=400)
        
        # Get and validate the `source_name`:
        source_name = request_data.get('source_name')
        if source_name is None:
            response_data = {
                'result': 'error',
                'message': 'No `source_name` provided.'
            }
            return JsonResponse(response_data, status=400)
        elif not isinstance(source_name, str):
            response_data = {
                'result': 'error',
                'message': 'Invalid `source_name`.'
            }
            return JsonResponse(response_data, status=400)
        
        # Get and validate the `source_location`:
        source_location = request_data.get('source_location')
        if source_location is None:
            response_data = {
                'result': 'error',
                'message': 'No `source_location` provided.'
            }
            return JsonResponse(response_data, status=400)
        elif not isinstance(source_location, str):
            response_data = {
                'result': 'error',
                'message': 'Invalid `source_location`.'
            }
            return JsonResponse(response_data, status=400)

        # Create the source:

        # Create the source:
        try:
            source_instance = DataSourceModel(name=source_name, location=source_location)
            source_instance.save()
        except ValidationError:
            response_data = {
                'result': 'error',
                'message': 'Failed to validate source data.'
            }
            return JsonResponse(response_data, status=400)
        except Exception:
            response_data = {
                'result': 'error',
                'message': f'Failed to create source.'
            }
            return JsonResponse(response_data, status=500)

        # Return the success response:
        response_data = {
            'result': 'success',
            'message': 'The source was created successfully.'
        }
        return JsonResponse(response_data, status=200)
    else:
        response_data = {
            'result': 'error',
            'message': f'Unknown HTTP method: `{request.method}`.'
        }
        return JsonResponse(response_data, status=400)

@login_required
def source_detail(request):
    """
    RESTful API endpoint for interacting with a single source.

    This endpoint will perform different actions depending on the HTTP request
    method used to access the endpoint.
    """

    # Get the json data:
    try:
        request_data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        response_data = {
            'result': 'error',
            'message': 'Invalid JSON request body.'
        }
        return JsonResponse(response_data, status=400)

    if request.method == 'GET':
        """
        The `GET` method will fetch the data from the data-source. This can be
        used to construct a graph.
        """

        # Get the source ID:
        source_id = request_data.get('source_id')
        if source_id is None:
            response_data = {
                'result': 'error',
                'message': 'No `source_id` provided.'
            }
            return JsonResponse(response_data, status=400)
        elif not isinstance(source_id, int):
            response_data = {
                'result': 'error',
                'message': 'Invalid `source_id`.'
            }
            return JsonResponse(response_data, status=400)
        
        # Check if transformations should be applied to the source data:
        transform = request_data.get('transform')
        if transform is None:
            transform = False
        
        # Get the source data:
        try:
            data_source = DataSourceModel.objects.get(id=source_id)
        except DataSourceModel.DoesNotExist:
            response_data = {
                'result': 'error',
                'message': f'No source found for ID `{source_id}`.'
            }
            return JsonResponse(response_data, status=400)

        # TODO: Get the data at the source here
        # TODO: Add transformation here

        response_data = {
            'result': 'success'
        }
        return JsonResponse(response_data, status=200)
    elif request.method == 'PUT':
        """
        The `PUT` method will replace all current representations of the target
        resource with the request payload. Simply put, this will create or
        update the CSV resource with the request payload.
        """

        # TODO: Check that the user has permission to perform this action

        # Get and validate the `source_name`:
        source_name = request_data.get('source_name')
        if source_name is None:
            response_data = {
                'result': 'error',
                'message': 'No `source_name` provided.'
            }
            return JsonResponse(response_data, status=400)
        elif not isinstance(source_name, str):
            response_data = {
                'result': 'error',
                'message': 'Invalid `source_name`.'
            }
            return JsonResponse(response_data, status=400)
        
        # Get and validate the `source_location`:
        source_location = request_data.get('source_location')
        if source_location is None:
            response_data = {
                'result': 'error',
                'message': 'No `source_location` provided.'
            }
            return JsonResponse(response_data, status=400)
        elif not isinstance(source_location, str):
            response_data = {
                'result': 'error',
                'message': 'Invalid `source_location`.'
            }
            return JsonResponse(response_data, status=400)

        # Create the source:
        source_data = {
            'name': source_name,
            'location': source_location
        }
        try:
            source_instance = DataSourceModel.objects.get_or_create(name=source_name, defaults=source_data)
            source_instance.save()
        except ValidationError:
            response_data = {
                'result': 'error',
                'message': 'Failed to validate source data.'
            }
            return JsonResponse(response_data, status=400)
        except Exception:
            response_data = {
                'result': 'error',
                'message': 'Failed to update source.'
            }
            return JsonResponse(response_data, status=500)

        # Return the success response:
        response_data = {
            'result': 'success',
            'message': 'The source was updated successfully.'
        }
        return JsonResponse(response_data, status=200)
    elif request.method == 'DELETE':
        """
        The `DELETE` method will delete the described source.
        """
        # TODO
        response_data = {
            'result': 'error',
            'message': 'Not implemented.'
        }
        return JsonResponse(response_data, status=500)
    else:
        response_data = {
            'result': 'error',
            'message': f'Unrecognised HTTP request method: `{request.method}`.'
        }
        return JsonResponse(response_data, status=400)

@login_required
def graph_list(request):
    # TODO
    response_data = {
        'result': 'error',
        'message': 'Not implemented.'
    }
    return JsonResponse(response_data, status=500)

@login_required
def graph_detail(request):
    # TODO
    response_data = {
        'result': 'error',
        'message': 'Not implemented.'
    }
    return JsonResponse(response_data, status=500)