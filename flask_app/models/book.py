from flask_app.config.mysqlconnection import connectToMySQL # import databse connection
from flask_app.models import author # import author to create instances in favs list
class Book:
    DB = 'books_schema'
    def __init__(self, data) -> None:
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.update_at = data['updated_at']
        self.favorite_authors = []

    # Queries below will connect to database and return requested information
    # Class methods for CRUD
    # CREATE
    @classmethod
    def create_book(cls, data):
        query = """INSERT INTO books (title, num_of_pages)
            VALUES (%(title)s, %(num_pages)s)"""
        new_book_id = connectToMySQL(cls.DB).query_db(query, data)
        return new_book_id
    # READ
    @classmethod
    def get_all_books(cls):
        query = "SELECT * FROM books" # query to call all rows from table
        results = connectToMySQL(cls.DB).query_db(query) # returns a list of rows
        all_books = [] # will store all instances of Book
        for book in results:
            all_books.append(cls(book)) # create a Book instance for each item in results list
        return all_books
    @classmethod
    def get_book_by_id(cls, id):
        query = "SELECT * FROM books where id=%(id)s"
        results = connectToMySQL(cls.DB).query_db(query, {'id': id}) # results will be a list of one
        return cls(results[0]) # make instance and return single record
    @classmethod
    def get_book_favs(cls, id): # query will return the book id info even if no favorites exist
        query = """SELECT * FROM books
                LEFT JOIN favorites on books.id = book_id
                LEFT JOIN authors on authors.id = author_id
                WHERE books.id = %(id)s"""
        results = connectToMySQL(cls.DB).query_db(query, {'id': id}) # send query to grab all favs of books
        book = cls(results[0]) # create a Book instance with first row. Works even if no favorites are present (;eft join)
        for db_row in results:
            author_data = {
                'id': db_row['author_id'],
                'name': db_row['name'],
                'created_at': db_row['created_at'],
                'updated_at': db_row['updated_at']
            }
            book.favorite_authors.append(author.Author(author_data))
        return book
    # UPDATE
    # DELETE