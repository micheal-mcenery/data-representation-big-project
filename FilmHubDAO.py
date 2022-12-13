import mysql.connector
import dbconfig_template as cfg
class FilmHubDAO:
    connection=""
    cursor =''
    host=       ''
    user=       ''
    password=   ''
    database=   ''
    
    def __init__(self):
        self.host=       cfg.mysql['host']
        self.user=       cfg.mysql['user']
        self.password=   cfg.mysql['password']
        self.database=   cfg.mysql['database']

    def getcursor(self): 
        self.connection = mysql.connector.connect(
            host=       self.host,
            user=       self.user,
            password=   self.password,
            database=   self.database,
        )
        self.cursor = self.connection.cursor(buffered=True)
        return self.cursor

    def closeAll(self):
        self.connection.close()
        self.cursor.close()
      
    def createMovies(self, values):
        cursor = self.getcursor()
        sql="insert into movies (title, director, genre, image) values (%s,%s,%s,%s)"
        cursor.executemany(sql, values)

        self.connection.commit()
        newid = cursor.lastrowid
        self.closeAll()
        return newid

    def createMovie(self, values):
        cursor = self.getcursor()
        sql="insert into movies (title, director, genre, image) values (%s,%s,%s,%s)"
        cursor.execute(sql, values)

        self.connection.commit()
        newid = cursor.lastrowid
        self.closeAll()
        return newid

    def getAllMovies(self):
        cursor = self.getcursor()
        sql="select * from movies"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        print(results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionary(result))
        
        self.closeAll()
        return returnArray

    def findByID(self, id):
        cursor = self.getcursor()
        sql="select * from movies where id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        returnvalue = self.convertToDictionary(result)
        self.closeAll()
        return returnvalue

    def findByTitle(self, title):
        cursor = self.getcursor()
        sql="select * from movies where title = %s"
        values = (title,)

        cursor.execute(sql, values)
        resultSet = cursor.fetchall()
        returnArray = []
        print(resultSet)
        for result in resultSet:
            print(result)
            returnArray.append(self.convertToDictionary(result))
        
        self.closeAll()
        return returnArray

    def findByDirector(self, director):
        cursor = self.getcursor()
        sql="select * from movies where director = %s"
        values = (director,)
        
        cursor.execute(sql, values)
        resultSet = cursor.fetchall()
        returnArray = []
        print(resultSet)
        for result in resultSet:
            print(result)
            returnArray.append(self.convertToDictionary(result))
        
        self.closeAll()
        return returnArray

    def findByGenre(self, genre):
        cursor = self.getcursor()
        sql="select * from movies where genre = %s"
        values = (genre,)

        cursor.execute(sql, values)
        resultSet = cursor.fetchall()
        returnArray = []
        print(resultSet)
        for result in resultSet:
            print(result)
            returnArray.append(self.convertToDictionary(result))
        
        self.closeAll()
        return returnArray

    def updateMovie(self, values):
        cursor = self.getcursor()
        sql="update movies set genre=%s where id = %s" 
        cursor.execute(sql, values)

        self.connection.commit()
        self.closeAll()

        return "Updated movie with id: "+str(values[1])
        
    def deleteMovie(self, title):
        cursor = self.getcursor()
        sql="delete from movies where title = %s"
        values = (title,)

        cursor.execute(sql, values)

        self.connection.commit()
        self.closeAll()
        return "Deleted movie with title: "+title

    def deleteAvailability(self, movieId):
        cursor = self.getcursor()
        sql="delete from availability where movie_id = %s"
        values = (movieId,)

        cursor.execute(sql, values)

        self.connection.commit()
        self.closeAll()
        return "Deleted movie availability for id: "+str(movieId)

    def findByStreamingService(self, service):
        cursor = self.getcursor()
        sql="SELECT m.id, title, director, genre, image from movies m inner join availability a on m.id = a.movie_id inner join streaming_site s on a.service_id = s.id where service_name IN(%s)"
        values = (service,)

        cursor.execute(sql, values)
        resultSet = cursor.fetchall()
        returnArray = []
        print(resultSet)
        for result in resultSet:
            print(result)
            returnArray.append(self.convertToDictionary(result))
        
        self.closeAll()
        return returnArray

    def findMovieAvailability(self, title):
        cursor = self.getcursor()
        sql="SELECT service_name from movies m inner join availability a on m.id = a.movie_id inner join streaming_site s on a.service_id = s.id where title IN(%s)"
        values = (title,)

        cursor.execute(sql, values)
        resultSet = cursor.fetchall()
        returnArray = []
        print(resultSet)
        for result in resultSet:
            print(result)
            returnArray.append(self.convertToDictionaryServiceName(result))
        
        self.closeAll()
        return returnArray

    def findStreamingServiceByName(self, name):
        cursor = self.getcursor()
        sql="select id from streaming_site where service_name = %s"
        values = (name,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        
        returnvalue = self.convertToDictionaryId(result)
        self.closeAll()
        return returnvalue

    def findSecretByApiName(self, name):
        cursor = self.getcursor()
        sql="select secret from apikeys where service = %s"
        values = (name,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        
        returnvalue = self.convertToDictionaryApiKeys(result)
        self.closeAll()
        return returnvalue

    # only applicable to movie result set
    def convertToDictionary(self, result):
        colnames=['id','title','director', "genre","image"]
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item

    def convertToDictionaryApiKeys(self, result):
        colnames=['secret']
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item

    def getAllStreamingServices(self):
        cursor = self.getcursor()
        sql="select service_name from streaming_site"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        print(results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionaryServiceName(result))

        self.closeAll()
        return returnArray


    def convertToDictionaryId(self, result):
        colnames=['id']
        item = {}
        print(f"RESULT>>>>> {result}")
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item

    def convertToDictionaryServiceName(self, result):
        colnames=['service_name']
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item
    
    def createMoviesTable(self):
        cursor = self.getcursor()
        sql="CREATE TABLE `movies` (   `id` int(11) NOT NULL AUTO_INCREMENT,   `title` varchar(250) DEFAULT NULL,   `director` varchar(250) DEFAULT NULL,   `genre` varchar(250) DEFAULT NULL,   `image` varchar(255) DEFAULT NULL,   PRIMARY KEY (`id`) ); "
        cursor.execute(sql)

        self.connection.commit()
        self.closeAll()

    def createAvailabilityTable(self):
        cursor = self.getcursor()
        sql="CREATE TABLE `availability` (  `id` INT NOT NULL AUTO_INCREMENT,  `service_id` INT NULL,  `movie_id` INT NULL,  PRIMARY KEY (`id`),  INDEX `fk_service_idx` (`service_id` ASC),  INDEX `fk_movie_idx` (`movie_id` ASC),  CONSTRAINT `fk_service`    FOREIGN KEY (`service_id`)    REFERENCES `streaming_site` (`id`)    ON DELETE NO ACTION    ON UPDATE NO ACTION,  CONSTRAINT `fk_movie`    FOREIGN KEY (`movie_id`)    REFERENCES `movies` (`id`)    ON DELETE NO ACTION    ON UPDATE NO ACTION);"
        cursor.execute(sql)

        self.connection.commit()
        self.closeAll()

    def createStreamingServiceTable(self):
        cursor = self.getcursor()
        sql="CREATE TABLE streaming_site (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, service_name VARCHAR(250));"
        cursor.execute(sql)

        self.connection.commit()
        self.closeAll()

    def createStreamingService(self, values):
        cursor = self.getcursor()
        sql="INSERT INTO streaming_site (service_name) VALUES (%s)"
        cursor.executemany(sql, values)

        self.connection.commit()
        newid = cursor.lastrowid
        self.closeAll()
        return newid

    def createAvailabilitys(self, values):
        cursor = self.getcursor()
        sql="insert into availability (service_id, movie_id) values (%s,%s)"
        cursor.executemany(sql, values)

        self.connection.commit()
        newid = cursor.lastrowid
        self.closeAll()
        return newid

    def createAvailability(self, values):
        cursor = self.getcursor()
        sql="insert into availability (service_id, movie_id) values (%s,%s)"
        cursor.execute(sql, values)

        self.connection.commit()
        newid = cursor.lastrowid
        self.closeAll()
        return newid

    def createUserTable(self):
        cursor = self.getcursor() 
        sql = "CREATE TABLE `account` (   `id` INT NOT NULL AUTO_INCREMENT,   `user_name` VARCHAR(45) NOT NULL,   `password` VARCHAR(45) NOT NULL,   PRIMARY KEY (`id`));"
        cursor.execute(sql)

        self.connection.commit()
        self.closeAll()

    def checkLogin(self, values):
        cursor = self.getcursor()
        sql = "SELECT id FROM account WHERE user_name = %s AND password = %s"
        cursor.execute(sql, values)

        result = cursor.fetchone()
        returnvalue = self.convertToDictionaryId(result)
        self.closeAll()
        return returnvalue

    def createAPIKeyTable(self):
        cursor = self.getcursor() 
        sql = "CREATE TABLE `apikeys` (   `id` INT NOT NULL AUTO_INCREMENT,   `service` VARCHAR(45) NOT NULL,   `secret` VARCHAR(45) NOT NULL,   PRIMARY KEY (`id`));"
        cursor.execute(sql)

        self.connection.commit()
        self.closeAll()

    def createdatabase(self):
        self.connection = mysql.connector.connect(
                host=       self.host,
                user=       self.user,
                password=   self.password,
        )
        self.cursor = self.connection.cursor()
        
        sql= "create database "+ self.database+";"
        self.cursor.execute(sql)

        self.connection.commit()
        self.closeAll()

    def dropDatabase(self):
            self.connection = mysql.connector.connect(
                    host=       self.host,
                    user=       self.user,
                    password=   self.password,
            )
            self.cursor = self.connection.cursor()
            
            sql= "DROP "+ self.database
            self.cursor.execute(sql)

            self.connection.commit()
            self.closeAll()        
        
filmHubDAO = FilmHubDAO()

if __name__ == "__main__":
    filmHubDAO.dropDatabase()
    filmHubDAO.createdatabase()
    filmHubDAO.createMoviesTable()

    data = [("Pulp Fiction", "Quentin Tarantino", "Crime","null"), 
            ("Kill Bill", "Quentin Tarantino", "Thriller","null"), 
            ("Inglourious Basterds", "Quentin Tarantino", "War","null"),
            ("E.T the Extra-Terrestrial", "Steven Spielberg", "Science Fiction","null"),
            ("Jurassic Park", "Steven Spielberg", "Science Fiction","null"),
            ("Saving Private Ryan", "Steven Spielberg", "War","null"),
            ("Goodfellas", "Martin Scorsese", "Crime","null"),
            ("Shutter Island", "Martin Scorsese", "Thriller","null"),
            ("The Wolf of Wall Street", "Martin Scorsese", "Crime","null"),
            ("2001 A Space Odyssey", "Stanley Kubrick", "Science Fiction","null"),
            ("The Shining", "Stanley Kubrick", "Horror","null"),
            ("Full Metal Jacket", "Stanley Kubrick", "War","null"),
            ("Alien", "Ridley Scott", "Horror","null"),
            ("Blade Runner", "Ridley Scott", "Science Fiction","null"),
            ("The House of Gucci", "Ridley Scott", "Drama","null"),
            ("Titanic", "James Cameron", "Drama","null"),
            ("Aliens", "James Cameron", "Horror","null"),
            ("Avatar", "James Cameron", "Science Fiction","null"),
            ("Tenet", "Christopher Nolan", "Science Fiction","null"),
            ("Dunkirk", "Christopher Nolan", "War","null"),
            ("Interstellar", "Christopher Nolan", "Science Fiction","null")
            ]
    filmHubDAO.createMovies(data)

    filmHubDAO.createStreamingServiceTable()

    sites = [('Netflix',),('Amazon Prime Video',),('Disney',),('Paramount',),('Sky Go',),('Apple TV',)]

    
    filmHubDAO.createStreamingService(sites)

    filmHubDAO.createAPIKeyTable()

    filmHubDAO.createUserTable()

    filmHubDAO.createAvailabilityTable()

    availability = [(1,1), (4, 1), (5, 2), (1, 3), (6, 4), (5, 5), (5, 6), (6, 7), (1, 8), (1, 9), (6, 10), (6, 11), (6, 12), (3, 13), (6, 14), (2, 15), (6, 16), (3, 17), (3, 18), (2, 19), (2, 20), (5, 21)]

    filmHubDAO.createAvailabilitys(availability)

   