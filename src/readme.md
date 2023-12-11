# CSV Mapper - Django Project
This directory contains the Django project for the CSV mapper application. This
has been split into many different "Django apps":
- `account`: Manages user registration, login, and authentication. Includes
  views, templates, and forms for handling user accounts.
- `api`: RESTful API used to interact with the MySQL database and fetch graph
  and source data.
- `dashboard`: Handles the main functionality of rendering data to live graphs.
  Contains views, templates, and static files related to the user dashboard.