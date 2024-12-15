import requests
from io import StringIO
from urllib.parse import urlparse
from urllib.error import URLError

from api.views.response import error_response

ALLOWED_CSV_CHARSET='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-./\\({)}[]+<>,!?£$%^&* '

def clean_csv_value(value):
    """
    Cleans a CSV entry by retaining only allowed characters and trimming any
    leading or trailing whitespace.
    
    Arguments:
    - value (any): The input value to clean.
    
    Returns:
    str: The cleaned value as a string.
    """
    
    # Validate the value is a valid string:
    if value is None:
        return ''
    value = str(value)
    
    # Remove disallowed characters and trim whitespace:
    return ''.join([char for char in value if char in ALLOWED_CSV_CHARSET]).strip()

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
    
    if url.scheme not in ('http', 'https'):
        return False, error_response(f'Cannot open location because `{url.scheme}` is not a supported URL scheme.', 400)
    
    # Read the CSV data from the source:
    try:
        response = requests.get(location, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        if 'text/csv' not in response.headers.get('Content-Type', ''):
            return False, error_response('The provided URL does not return a valid CSV file.', 400)
        csv_content = response.text
    except requests.exceptions.RequestException as exception:
        return False, error_response(f'Failed to read CSV data from location `{location}`: {exception}.', 400)

    # Convert the CSV content into a CSV file:
    csv_file = StringIO(csv_content)

    return True, csv_file