from django.http import JsonResponse

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

# TODO: The below method should be able to be removed, check references before removal
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