from flask import Flask # import flask to create an instance
app = Flask(__name__) # create an instanc of Flask
app.secret_key = "super secret key I won't use this project"