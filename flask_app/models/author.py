from flask_app.config.mysqlconnection import connectToMySQL # import databse connection
from flask_app.models import book # import book model to populate self.favorite_books

class Author:
    DB = 'books_schema'
    def __init__(self, data) -> None: # instance will model each row of the author database
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorite_books = []

    # Queries below will connect to database and return requested information
    # Class methods for CRUD
    # CREATE
    @classmethod
    def add_author(cls, data): # create instance of an author
        query = "INSERT INTO authors (name) VALUES (%(name)s)"
        new_author_id = connectToMySQL(cls.DB).query_db(query, data)
        return new_author_id
    @classmethod
    def add_favorite(cls, data): # query to add book to favorite list
        query = """INSERT INTO favorites (author_id, book_id)
                VALUES (%(author_id)s, %(book_id)s)"""
        return connectToMySQL(cls.DB).query_db(query, data)
        
    # READ
    @classmethod
    def get_all_authors (cls): # gets all records from authors table
        query = "SELECT * FROM authors"
        results = connectToMySQL(cls.DB).query_db(query)
        authors = [] # will store all instances of Author here
        for author in results:
            authors.append(cls(author)) # create an Author instance for each row
        return authors
    @classmethod
    def get_author_by_id(cls, id): # gets single row from authors table
        query = "SELECT * FROM authors WHERE id=%(id)s"
        results = connectToMySQL(cls.DB).query_db(query, {'id': id})
        this_author = cls(results[0]) # make an instance of the result
        return this_author # return instance to controller
    @classmethod
    def get_author_favs(cls, id): # add instances of favorite books into self.favorite_books
        query = """SELECT * FROM authors
                LEFT JOIN favorites on authors.id = author_id
                LEFT JOIN books on books.id = book_id
                WHERE authors.id = %(id)s"""
        results = connectToMySQL(cls.DB).query_db(query,{'id': id}) # returns all authors with their favorite books to a list
        author = cls(results[0]) # make an instance of Author using the first row
        for db_row in results: # make a book instance for each row
            book_data = { # makes a dictionary to send to Book
                "id": db_row['book_id'],
                "title": db_row['title'],
                "num_of_pages": db_row['num_of_pages'],
                "created_at": db_row['created_at'],
                "updated_at": db_row['updated_at']
            }
            author.favorite_books.append(book.Book(book_data)) # instance is created and added to favorites
        return author
    # UPDATE
    # DELETE