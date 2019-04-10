# udacity-project-2

Udacity Project 2: Flask Application Catalog
by George Haralampopoulos

Part of the Udacity Full Stack Web Developer Nanodegree.

External Libraries:

Flask v1.0.2
SqlAlchemy v1.2.18
OAuth2Client v4.1.3

Project contents:

run_application.py - The main Python script that serves the website. If no database is found, one is created and populated by populate_database.py.

client_secrets.json - Client secrets for Google OAuth login.

routes.py - route definitions for displaying the main application content

auth.py - Handles the login and logout of users using OAuth as well as helper functions.

sample_data.py - Adds default data to the sqlite database 

database_setup.py - Defines the Tables for the sqlite backend database.

database_helpers.py - Helper functions for the sqlite backend database.

Templates:

404.html - Renders a 404 not found message.

add.html - Page for a user to add new content

attractions.html - Main portal for viewing attractions in a specified category in the database.

base.html - Base template that sets up the local css styles and links for google api, bootstrap, and font-awesome

content.html - Displays info about a single attraction for authenticated users. Includes delete, and edit content buttons.

editForm - A portion of html that is used for editing content.

flash - a portion of html code that is used to flash messages using Flask.

home - the home page of the website, includes a welcome message and a preview display of the 5 most recently added attractions.

login - a simple login interface that redirects to homepage on authentication.

navbar - A reusable template for navigating content.

publiccontent - Displays info about a single attraction for all users.

Setup:

1) Initialize the sqlite database using the populate_database.py tool from the main catalog folder. This will create the backend database and also add some sample data so there is something to display when created.

Run:

1) python run_application.py --gapi_id <your-gapi-client-id> NOTE: the current application is hardcoded to run on localhost port 5000

Optional Args:
 	--debug : Enables Flask debug mode logging.
