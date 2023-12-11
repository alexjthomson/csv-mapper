# CSV Mapper - API
This application implements the API for the CSV mapper. The API is where all
database models are defined as well as RESTful API endpoints.

## Limitations
The RESTful API does not implement version checking since it is out of scope of
the project. In the future, versioning could be added via a prefix to the API
endpoints. For example: `/api/v1/` instead of `/api/`.