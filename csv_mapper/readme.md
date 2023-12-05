# CSV Mapper - Django Project
This directory contains the Django project for the CSV mapper application. This
has been split into many different "Django apps":
- `account` - Manages user registration, login, and authentication. Includes
  views, templates, and forms for handling user accounts.
- `api` - API used to fetch the translated graph data for a given graph. This
  API only manages graphing related data and is read-only.
- `dashboard` - Handles the main functionality of rendering data to live graphs.
  Contains views, templates, and static files related to the user dashboard.