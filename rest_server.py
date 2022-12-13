from flask import Flask, abort, jsonify, request, session
from FilmHubDAO import filmHubDAO

app = Flask(__name__, static_url_path='', static_folder='staticpages')
# used for the login functionality for extra protection 
app.secret_key = '123456'

@app.route('/')
def root():
    return app.send_static_file('index.html')

# get all Movies
@app.route('/movies', methods=['GET'])
def getAllMovies():
    movies = filmHubDAO.getAllMovies()
    return jsonify(movies)

# find Movie By id
@app.route('/movies/<int:id>', methods=['GET'])
def findById(id):
    movie = filmHubDAO.findByID(id)
    # we need to check the movies streaming service availability, and return this with the movie details
    availability = filmHubDAO.findMovieAvailability(movie['title'])
    movie['availability'] = availability

    return jsonify(movie)

# find Movie By title
@app.route('/movies/title/<string:title>', methods=['GET'])
def findByTitle(title):
    movie = filmHubDAO.findByTitle(title)
    # we need to check the movies streaming service availability, and return this with the movie details
    availability = filmHubDAO.findMovieAvailability(title)
    movie[0]['availability'] = availability

    return jsonify(movie)

# find Movie By Director
@app.route('/movies/director/<string:name>')
def findByDirector(name):
    movie = filmHubDAO.findByDirector(name)
    # we need to check the movies streaming service availability, and return this with the movie details
    availability = filmHubDAO.findMovieAvailability(movie[0]['title'])
    movie[0]['availability'] = availability

    return jsonify(movie)

#find Movie By Genre
@app.route('/movies/genre/<string:genre>')
def findByGenre(genre):
    movie = filmHubDAO.findByGenre(genre)
    # we need to check the movies streaming service availability, and return this with the movie details
    availability = filmHubDAO.findMovieAvailability(movie[0]['title'])
    movie[0]['availability'] = availability

    return jsonify(movie)

# create a movie
@app.route('/movies', methods=['POST'])
def createMovie():
    data = request.get_json()
    
    movie = (data['title'], data['director'], data['genre'],data['image'])
    movieId = filmHubDAO.createMovie(movie)

    # along with creating the movie we also need to create the movie availability based on the users selection
    for i in data['service']:
        service = (i['service_name'])
        serviceId = filmHubDAO.findStreamingServiceByName(service)
        availability = (serviceId['id'], movieId)
        filmHubDAO.createAvailability(availability)

    return jsonify({"id" : movieId})

# update a movie based on title (the genre and streaming service availability can be updated)
@app.route('/movies/<string:title>', methods=['PUT'])
def update(title):
    data = request.get_json()
    # streaming services defined by the user
    services = data['service']
    # genre defined by the user
    genre = data['genre']

    # get movie details and set the objects genre to the users value
    movie = filmHubDAO.findByTitle(title)
    movie[0]['genre'] = genre

    # remove existing links to the streaming service availability 
    filmHubDAO.deleteAvailability(movie[0]['id'])

    # create the availability based on the users selection
    for i in services:
        service = (i['service_name'])
        serviceId = filmHubDAO.findStreamingServiceByName(service)
        availability = (serviceId['id'], movie[0]['id'])
        filmHubDAO.createAvailability(availability)

    values =  (genre, movie[0]['id'])
    # finally update the movie
    movie = filmHubDAO.updateMovie(values)
    return jsonify(movie)

# delete a movie (if user is authorised)
@app.route('/movies/<string:title>', methods=['DELETE'])
def delete(title):
    if 'loggedin' in session:
        filmHubDAO.deleteAvailability(title)
        return filmHubDAO.deleteMovie(title)
    else:
        # 403 Forbidden is returned i.e. user is not authorised
        abort(403)

# find Movie By streaming site
@app.route('/movies/service/<string:service>')
def findByService(service):
    movie = filmHubDAO.findByStreamingService(service)
    return jsonify(movie)

# get all Streaming sites
@app.route('/movies/service', methods=['GET'])
def getAllStreamingServices():
    services = filmHubDAO.getAllStreamingServices()
    return jsonify(services)

# Login authorisation, return the account ID on success
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']
        values = (username, password,)
        account = filmHubDAO.checkLogin(values)
        
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            # Redirect to home page
            return jsonify(account)
        else:
            # Account doesnt exist or username/password incorrect
            return 'False'

# removes the users session
@app.route('/logout',methods=['GET'])
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return "logged out successfully"

# return true if the user has an active session i.e. the user is already logged in
@app.route('/login/status', methods=['GET'])
def loginStatus():
        
        if "loggedin" in session and session['loggedin']:
            return "True"
        else:
            return 'False'

# return the api key for the specified service
@app.route('/api/key/<string:service>', methods=["GET"])
def findByApiSecret(service):
    secret = filmHubDAO.findSecretByApiName(service)
    return jsonify(secret)




if __name__ == "__main__":
    app.run(debug=True)