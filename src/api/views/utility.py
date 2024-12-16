import nh3
import json
import requests
from io import StringIO
from urllib.parse import urlparse
from urllib.error import URLError

from api.views.response import error_response

ALLOWED_CSV_CHARSET='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-./\\({)}[]+<>,!?£$%^&* '

class SanitisedJSON:
    def __init__(self, data):
        """Initialise with the parsed JSON data."""
        
        self._data = data

    def __getitem__(self, key):
        """Get sanitised value for a field."""
        
        value = self._data.get(key)
        if isinstance(value, str):  # Sanitize only strings
            return nh3.clean(value)
        elif isinstance(value, dict):  # Recursively wrap nested dictionaries
            return SanitisedJSON(value)
        elif isinstance(value, list):  # Recursively clean lists
            return [nh3.clean(item) if isinstance(item, str) else item for item in value]
        return value

    def get(self, key, default=None):
        """Get sanitized value with a default."""
        return self[key] if key in self._data else default

    def as_dict(self):
        """Return the raw dictionary."""
        return self._data

def decode_json_body(request):
    """
    Gets the JSON body of a request.
    
    This should be used anywhere where JSON is fetched from the user since this
    sanitises each field fetched from it.
    
    Throws:
    - json.JSONDecodeError: Thrown if the JSON cannot be decoded from the
      request body.
    """
    
    # Get JSON request body:
    return SanitisedJSON(request.data)

def clean_csv_value(value):
    """
    Cleans a CSV entry by retaining only allowed characters and trimming any
    leading or trailing whitespace. Additionally, this will clean the text to
    prevent things such as XSS attacks.
    
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
    return nh3.clean(''.join([char for char in value if char in ALLOWED_CSV_CHARSET]).strip())

def read_source_at(location):
    """
    Reads a CSV source at the given location and returns the raw CSV data.
    
    This function will also clean the CSV resource fetched (if it was found),
    preventing things such as XSS.

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
    csv_file = StringIO(nh3.clean(csv_content))

    return True, csv_file