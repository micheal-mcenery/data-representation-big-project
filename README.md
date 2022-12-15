# Big Project (Micheal McEnery) #
This repository contains all of the files related to the Big Project for the Data Representation module. The creator of this repository is Micheál McEnery. This project is designed to reflect a movie catalogue, allowing a user to search for movies using various criteria, as well as adding, updating, and deleting movies from the database.
Below are details on how to run the program, as well as details on how each of the project requirements were achieved.

## Running the program ##
_Running from the web:_
  1.	Go to http://michealmcenery.pythonanywhere.com/
  2.  To login, please go to admin tab and enter the below login credentials:
        * Username: test
        * Password: test
  3.  Being logged in will give you full administration access, allowing you to delete movies from the database.

_Running locally:_
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

