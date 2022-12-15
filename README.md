# Big Project (Micheal McEnery) #
This repository contains all of the files related to the Big Project for the Data Representation module. The creator of this repository is Micheál McEnery. This project is designed to reflect a movie catalogue, allowing a user to search for movies using various criteria, as well as adding, updating, and deleting movies from the database.
Below are details on how to run the program, as well as details on how each of the project requirements were achieved.

## Running the program ##
__Running from the web:__
  1.	Go to http://michealmcenery.pythonanywhere.com/
  2.  To login, please go to admin tab and enter the below login credentials:
        * Username: test
        * Password: test
  3.  Being logged in will give you full administration access, allowing you to delete movies from the database.

__Running locally:__

Prerequisites: 
  1.	WAMP server is installed and running
  2.	Flask is installed

Instructions
  1.	Clone the GitHub repository and pull down the latest files.
  2.	In the root directory of the repository, create a file called dbconfig_template.py
  3.	Update the contents of this file so that it is similar to the below (set the values as per your environment):
        ```
        mysql = {
          "host" : "<host>",
          "user" : "<user>",
          "password" : "<password>",
          "database" : "filmhub"
        }
        ```
  4.	Open CMD from the root of the project directory, run FilmHubDAO.py using python e.g. python FilmHubDAO.py (this should create the database schema on tables on         your local environment)
  5.	FilmHub uses a 3rd party API, OMDB. You will need an api key for this to work correctly.
        1.	Go to https://www.omdbapi.com/apikey.aspx
        2.	Select FREE! (1,000 daily limit)
        3.	Enter your email address
        4.	Click Submit
        5.	Once you receive an email from OMDB with your api key, please go to step 6 (a)
  6.  Please run the following commands on your database server   (replace <your_key_here> with your OMDB api key):
        1.  ``INSERT INTO `apikeys` (`id`,`service`,`secret`) VALUES (null,"OMDB","<your_key_here>");``
        2.  ``INSERT INTO `account` (`id`,`user_name`,`password`) VALUES(null,"test","test");``
  7.	Return to the CMD window, and run the rest_server.py file using python e.g. python rest_server.py. You should see the following message:
        ```
        * Serving Flask app 'rest_server'
        * Debug mode: on
        WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
        * Running on http://127.0.0.1:5000
        Press CTRL+C to quit
        * Restarting with stat
        * Debugger is active!
        * Debugger PIN: 259-765-063
        ```
  8.  Copy the url (this is printed after Running on) and paste into Chrome and click enter.
  9.  FilmHub website should now be visible.
  10. To login, please go to admin tab and enter the below login credentials:
        * Username: test
        * Password: test
  11. Being logged in will give you full administration access, allowing you to delete movies from the database.

## Achieving Project Requirements ##
* A basic Flask server that has:
* REST API: The REST APIs are defined in the rest_server.py file. The REST APIs are referenced in the index.html file within the script tags. The postman collection on GitHub Movies.postman_collection also lists the available APIs.
* One database table: FilmHub has 5 database tables, these are created by the FilmHubDAO.py file, these are:
  * account (this is to support user login)
  * apikeys (this is where our OMDB key is stored so that it is not hardcoded in a file on GitHub)
  * availability (this tracks the movies streaming site availability)
  * movies (this is where the movie details are stored)
  * streaming_site (This is where streaming sites are defined (the id of this table is used along with the movie id in determining the movies streaming site availability in the availability table)
* Accompanying web interface, using AJAX calls, to perform these CRUD operations: The primary web interface is index.html. This is coded using HTML, CSS, Javascript, JQuery, Bootstrap and JQueryUI. 
This web page uses the REST APIs to perform CRUD operations via ajax calls.
Examples:
  * CREATE: the /movies endpoint using the POST method adds a movie
  * READ: the /movies endpoint using the GET method returns all movies
  * UPDATE: the /movies/<title> endpoint using the PUT method updates an existing movie
  * DELETE: the /movies/<title> endpoint using the DELETE method deletes a movie
* More than one database table: 
  * As outlined previously, FilmHub uses 5 different database tables.
* Authorization: 
  * Authorization is used to restrict the ability of the user to delete from the database. The account database table is used to store user credentials. Session data is created if the user supplies the correct username and password to the /login endpoint via POST method. 
A logout endpoint is implemented to remove user sessions.
A login status endpoint is also provided so that we can check whether the user is logged in or not and display the correct button to login or logout.
* Web page looks nice: 
  *	Bootstrap is used for the layout, button styling and modal dialogs. 
  *	JQueryUI is used for the tab element.
  *	CSS is used for styling e.g. the row of posters and the horizontal scroll bar.
* A more complicated API: 
  * The create and update movie API supports creating/updating streaming service availability as part of the create and update flow.
The delete API removes the movie along with the movies streaming service availability. The login status API checks if session object has the loggedin data.
* Server links to some third-party API: 
  * FilmHub uses the 3rd party API OMDB. OMDB provides movie details such as the plot, poster etc. similar to IMDB. The 3rd party API call is used when viewing the movie details (clicking on a movie poster, values used are listed under OMDB details in the modal).
* Third-party API requires authentication: 
  * An API key is required for using OMDB. Acquiring and storing the API key is outlined in the instructions above. The value is stored in the apikeys database table using an INSERT statement (this ensure the secret key is not publicly available on GitHub).
* Hosted online: 
  * FilmHub is also available on PythonAnywhere, available via: http://michealmcenery.pythonanywhere.com/
The instructions for running locally were followed to get the application deployed on PythonAnywhere. On the PythonAnywhere console I cloned the GitHub repository and then followed the steps I’ve outlined above.











