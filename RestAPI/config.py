from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)

# Build the Sqlite ULR for SqlAlchemy
uri = "postgres://postgres:Detlef228425@localhost/InspectorFYP_DB"

# Configure the SqlAlchemy part of the app instance
app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create the SqlAlchemy db instance
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    location = db.Column(db.String(50))


def index(name, location):
    user = User(name=name, location=location)
    db.session.add(user)
    db.session.commit()

    print("Added new user")
