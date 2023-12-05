# CSV Mapper - Design
CSV mapper maps CSV files containing critical infrastructure performance metrics
to a live graph.

## Technologies
- Python 3.12 (Latest Stable)
- Django 4.2 (Latest LTS)
- Bootstrap
- Chart.js
- MySQL
- Docker
- Docker Compose

## Application Design
The application itself is split into two parts: the front-end, and the back-end.
The back-end will use Python and Django and need to interact with a MySQL
database. The front-end will use Bootstrap and Chart.js to provide a responsive and reactive
front-end user experience.

## Database Design
The application requires:
- User Accounts & Account Types
- Graphs
- CSV Sources

Therefore, the application requires at least 3 tables:
- `user` - Contains user account information such as the username, password,
  and password hash.
- `graph` - Contains each of the graphs that have been created along with any
  configuration for the graph such as update intervals.
- `data_source` - Contains the endpoint to find a CSV file.
- `data_config` - Each row contains configuration for a single column within a
  CSV file. This can be used to transform the data into a more useful format
  that can be used by the application.

Ideally the database would have the following additional tables; however, the
requirements for the application limit it to 4 tables:
- `user_details` - Contains additional information about a user such as their
  first name, last name, and job title.
- `user_graph_config` - Contains configuration for a graph that a user has used.
  This table would store configuration for each series displayed on a graph. In
  this case, a series corresponds to a column within a CSV file.
- `user_settings` - Contains user settings such as a default graph to open after
  login, the theme of the application, etc.

### Table Design

#### User Table (user)
This table contains user account information used to log into the application.

| Column Name       | Type      | Description | Usage |
| ----------------- | --------- | ----------- | ----- |
| id                | PRI int   | Unique ID of the user. | Identifies the user. Can be used as a foreign key in other tables to identify the user. |
| username          | varchar   | Unique username for the user. | Allows the user to login using a memorable name. |
| password          | varchar   | Hashed password. | Used to authenticate the user. |
| salt              | varchar   | Password salt. | Adds complexity to the users password. This makes it much harder to brute-force crack the password hash. |
| type              | enum      | Describes if the user is a standard user, or an admin. This has scope to be expanded on in the future since it is an enum. | Used to determine user permissions. |
| approved          | tinyint   | Describes if the user has been approved or not. | When `true`, the user is allowed to login. By default this is `false`. This allows site admins to approve new accounts. |
| created_timestamp | timestamp | The time that the user account was created. | Provides greater detail to site-admins about when an account was created. |

##### Notes
The user table does not contain an email since this application relies on an
internal administrator account approving new accounts.

#### Graph Table (graph)
This table contains a row for each graph that has been created.

| Column Name    | Type    | Description | Usage |
| -------------- | ------- | ----------- | ----- |
| id             | PRI int | Unique ID of the graph. | Identifies the graph. Can be used as a foreign key in other tables to identify the graph. |
| name           | varchar | Unique display name of the graph. | Provides an easy to remember and descriptive name that can be used to identify the graph. |
| data_source_id | int     | ID of the data-source that the graph gets it data from. | Allows the graph to be linked to a data-source. |

#### Data-Source Table (data_source)
This table contains where to find CSV data that can be displayed onto a graph.

| Column Name    | Type    | Description | Usage |
| -------------- | ------- | ----------- | ----- |
| id             | PRI int | Unique ID of the data-source. | Identifies the data source. Can be used as a foreign key in other tables to identify the data-source. |
| name           | varchar | Unique display name of the data-source. | Provides an easy to remember and descriptive name that can be used to identify the data-source when creating a graph. |
| location       | varchar | Describes where to find the CSV data. | Identifies where the CSV data can be found. This may be on the local system, an HTTP endpoint, or a remote destination on an FTP server. |

#### Data-Source Configuration Table (data_config)
This tables allows for individual columns within a data-source to be configured.
This is required since not all CSV files will have nice column names (if any).
The actual data within the column may also need transforming into a usable
format.

| Column Name    | Type    | Description | Usage |
| -------------- | ------- | ----------- | ----- |
| id             | PRI int | Unique ID of the configuration entry. | Identifies the configuration entry, thereby allowing deletion and modification of the entry. |
| data_source_id | int     | ID of the data-source that the configuration entry applies to. | Associates the configuration entry with a data-source. |
| column_id      | tinyint | ID of the column within the CSV data that this entry applies to. | Identifies which column within the CSV data to apply the configuration to. |
| column_name    | varchar | Non-unique display name to apply to the column. | Allows a human-readable display name to be defined for the CSV file without editing the CSV file itself. |
| transform_type | enum    | Type of transformation to apply to the data within the column. | Allows data to be transformed into a more useful format using a set transform. |
| unit           | varchar | Unit to apply to the data. | This allows a unit to be applied to the column. For instance, if the column is describing a bitrate in megabits per second, `Mbps` may be used. |