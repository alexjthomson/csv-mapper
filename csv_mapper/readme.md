# CSV Mapper - Django Project
This directory contains the Django project for the CSV mapper application. This
has been split into many different "Django apps":
- `account` - Manages user registration, login, and authentication. Includes
  views, templates, and forms for handling user accounts.
- `admin` - Allows administrator accounts to approve users, create graphs,
  register CSV data-sources, and any other site-management related activities.
  This includes views, templates, and forms for site-management. This app is
  also the only app that is capable of deleting from the SQL database.
- `api` - API used to fetch the translated graph data for a given graph. This
  API only manages graphing related data and is read-only.
- `dashboard` - Handles the main functionality of rendering data to live graphs.
  Contains views, templates, and static files related to the user dashboard.