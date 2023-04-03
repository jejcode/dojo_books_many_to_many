from flask import render_template, redirect, request # import flask modules to run routes
from flask_app import app # import app so routes will work
from flask_app.models import book, author

@app.route('/books')
def show_all_books(): 
    all_books = book.Book.get_all_books() # get all records from books table
    return render_template('all_books.html', books = all_books)

@app.route('/books/create', methods=['POST']) # process form data
def create_book():
    new_book_id = book.Book.create_book(request.form) # insert new book into books table
    return redirect(f"/books/{new_book_id}") # redirect to book page using new book's id

@app.route('/books/<int:id>') # route displays individual book and all authors that favorite it
def show_book(id):
    book_data = book.Book.get_book_favs(id) # sends query, and returns book info even if no favs
    authors_list = author.Author.get_all_authors() # base list of authors to populate form list
    fav_ids = [] # will capture id's of favorited author
    non_favs = [] # list to store non-favorited author's
    for entry in book_data.favorite_authors: 
        fav_ids.append(entry.id) # grab id's of favorited authors
    for item in authors_list:
        if item.id not in fav_ids:
            non_favs.append(item) # store instances that have not been favorited
    return render_template('show_book.html', book_data = book_data, authors_list = non_favs)

@app.route('/books/add_favorite', methods=['POST'])
def add_favorite_author():
    # take book id and author id and put it in favorites table
    author.Author.add_favorite(request.form)
    return redirect(f"/books/{request.form['book_id']}")