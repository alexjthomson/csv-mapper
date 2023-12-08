from django.core.exceptions import ValidationError
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

        # Check permissions:
        if not request.user.has_perm('api.view_datasourcemodel'):
            response_data = {
                'result': 'error',
                'message': 'User does not have permission to perform this action.'
            }
            return JsonResponse(response_data, status=403)

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

        # Check permissions:
        if not request.user.has_perm('api.add_datasourcemodel'):
            response_data = {
                'result': 'error',
                'message': 'User does not have permission to perform this action.'
            }
            return JsonResponse(response_data, status=403)
        
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
        return JsonResponse(response_data, status=405)

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
        if not request.user.has_perm('api.view_datasourcemodel'):
            response_data = {
                'result': 'error',
                'message': 'User does not have permission to perform this action.'
            }
            return JsonResponse(response_data, status=403)

        source = DataSourceModel.objects.get(id=source_id)
        if source is not None:
            response_data = {
                'result': 'success',
                'data': {
                    'name': source.name,
                    'location': source.location,
                }
            }
            return JsonResponse(response_data, status=200)
        else:
            response_data = {
                'result': 'error',
                'message': f'Source `{source_id}` does not exist.'
            }
            return JsonResponse(response_data, status=404)
    elif request.method == 'DELETE':
        """
        The `DELETE` method will delete a single source.

        If the resource is deleted successfully, a 200 response code is
        returned; otherwise, if the resource is not found, 404 is returned.

        The user must have permission to delete the corresponding model to
        interact with this API endpoint.
        """
        
        # Check permissions:
        if not request.user.has_perm('api.delete_datasourcemodel'):
            response_data = {
                'result': 'error',
                'message': 'User does not have permission to perform this action.'
            }
            return JsonResponse(response_data, status=403)
        
        # Get the source:
        source = DataSourceModel.objects.get(id=source_id)
        if source is not None:
            # The source exists, we can now delete it:
            source.delete()
            response_data = {
                'result': 'success',
                'message': f'Deleted source `{source_id}`.'
            }
            return JsonResponse(response_data, status=200)
        else:
            # The source does not exist.
            response_data = {
                'result': 'error',
                'message': f'Source `{source_id}` does not exist.'
            }
            return JsonResponse(response_data, status=404)
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
        if not request.user.has_perm('api.change_datasourcemodel'):
            response_data = {
                'result': 'error',
                'message': 'User does not have permission to perform this action.'
            }
            return JsonResponse(response_data, status=403)
        
        # Get JSON request body:
        try:
            json_request = json.loads('json', request.body.decode('utf-8'))
        except json.JSONDecodeError:
            response_data = {
                'result': 'error',
                'message': 'Invalid JSON request body.'
            }
            return JsonResponse(response_data, status=400)

        # Get JSON fields:
        source_name = json_request['name']
        if source_name is None:
            response_data = {
                'result': 'error',
                'message': 'Expected `name` field.'
            }
            return JsonResponse(response_data, status=400)
        elif not isinstance(source_name, str):
            response_data = {
                'result': 'error',
                'message': 'Invalid `name` field; expected a string.'
            }
            return JsonResponse(response_data, status=400)

        source_location = json_request['location']
        if source_name is None:
            response_data = {
                'result': 'error',
                'message': 'Expected `location` field.'
            }
            return JsonResponse(response_data, status=400)
        elif not isinstance(source_name, str):
            response_data = {
                'result': 'error',
                'message': 'Invalid `location` field; expected a string.'
            }
            return JsonResponse(response_data, status=400)

        # Get the source:
        source = DataSourceModel.objects.get(id=source_id)
        if source is not None:
            # The source exists, we can now modify it:
            source.name = sourcE_name
            source.location = source_location
            source.save()
            response_data = {
                'result': 'success',
                'message': f'Deleted source `{source_id}`.'
            }
            return JsonResponse(response_data, status=200)
        else:
            # The source does not exist.
            response_data = {
                'result': 'error',
                'message': f'Source `{source_id}` does not exist.'
            }
            return JsonResponse(response_data, status=404)
    else:
        response_data = {
            'result': 'error',
            'message': f'Unknown HTTP method: `{request.method}`.'
        }
        return JsonResponse(response_data, status=405)


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