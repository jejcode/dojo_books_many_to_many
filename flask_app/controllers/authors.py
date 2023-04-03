from flask import render_template, redirect, request # import flask modules to run routes
from flask_app import app # import app so routes will work
from flask_app.models import author, book

@app.route('/')
def default_load():
    return redirect('/authors')

@app.route('/authors') # route shows a list of authors and an add author form
def all_authors():
    # query db to get all authors
    all_authors = author.Author.get_all_authors() # get all authors from db
    return render_template('all_authors.html', authors=all_authors)

@app.route('/authors/add', methods=['POST']) # process the add author form
def add_author():
    new_author_id = author.Author.add_author(request.form)
    return redirect(f"/authors/{new_author_id}") # redirect to page that shows author's favorites

@app.route('/authors/<int:id>') # display author's favorites and has a form to add favorites
def show_author(id):
    author_data = author.Author.get_author_favs(id) # query DB for author data
    books_list = book.Book.get_all_books() # get all of this author's favorite books
    fav_ids = [] # capture id's of fav books
    non_favs = [] # empty list to make a list of non-fav books
    for item in author_data.favorite_books: # capture ids of fav books
        fav_ids.append(item.id) # place fav ids into a list
    for entry in books_list:
        if entry.id not in fav_ids: # if id is not on fav list, add it to the list for the page form
            non_favs.append(entry)
    return render_template('show_author.html', author_data = author_data, books_list = non_favs)

@app.route('/authors/add_favorite', methods=['POST'])
def add_favorite_book():
    # take book id and author id and put it in favorites table
    author.Author.add_favorite(request.form)
    return redirect(f"/authors/{request.form['author_id']}")