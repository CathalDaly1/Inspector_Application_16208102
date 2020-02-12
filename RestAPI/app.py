import os
# import connexion
from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
from flask import Flask
from flask_restful import Api, Resource, reqparse

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
api = Api(app)
uri = "postgres://postgres:Detlef228425@localhost/InspectorFYP_DB"

# Configure the SqlAlchemy part of the app instance
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = uri

db = SQLAlchemy(app)
