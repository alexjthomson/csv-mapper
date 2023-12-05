# CSV Mapper - Planning
CSV mapper maps CSV files containing critical infrastructure performance metrics
to a live graph.

## Context
Gamma Telecom has many business critical SQL systems. They have developed a tool
to export performance information for these systems as CSV files. This tool runs
24/7 and there currently isn't a good way of using these files.

## Introduction
This project aims to read CSV files containing performance information for
business critical systems. These CSV files are not easily human-readable for
debugging and performance monitoring purposes; therefore, a tool needs to be
developed to allow them to be used effectively.

The CSV mapper tool aims to provide an ergonomic web-based interface to manage
and view these CSV files as graphs.

## Requirements
- Must be accessible in a web browser.
- Must have a login function.
- Must have standard users and admin users.
- Users must be able to register and login in order to use the application.
- Admin users should have the ability to perform all CRUD (create, read, update,
  and delete) operations on the database tables and make changes to the
  underlying database data.
- Admins must have to approve new users.
- There should be a way of creating a new user via local command-line tools.
  This is required to create the initial administrator user.
- Regular users should only have the ability to perform create, read, and update
  operations only.
- Validation should be performed in both the web browser and the server. This
  needs to be performed for usernames, passwords, and any other field that the
  end-user can populate.
- Administrators should be able to add and remove CSV files that the application
  can access.
- Administrators should be able to create, delete, and modify monitoring graphs.
- Monitoring graphs require a CSV file to graph data.
- Monitoring graphs can be configured with an update interval. This is the
  interval of time between updates. An update means reading the CSV file again.
- The application should have read-only access to the CSV files. It should not
  write to the CSV files.
- The application needs logging. Logs should be output to STDOUT and STDERR.
  Logs should also be written to disk.
- The application should run within a Docker container.
- The application should be built for Linux.
- The application should be written in Python.
- The application should have a minimum of 2 tables, and a maximum of 4 tables
  using any relational database technology of choice.

## User Stories
A set of user stories have been defined to better understand the requirements of
the project with context.

| User | Action | Summary |
| ---- | ------ | ------- |
| SQL System Stakeholder | Creating an account. | Able to access graphing software and monitor the systems that they are a stakeholder for. |
| Site Admin | Approving an account registration. | Able to control who has access to the tool. |
| Site Admin | Managing another account. | Able to remove users that no longer need access to the tool. Able to assist the user with login issues. |
| SQL Developer | Checking performance of business critical SQL systems. | Able to quickly identify discrepancies in performance that they may need to focus on. Aids in debugging. |

## Additional Considerations
Some CSV files will likely have lots of different columns. This will clutter the
graph and potentially make it unusable. Columns should be able to be toggled
on/off by the user to declutter the graph.