from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
import psycopg2
from paths import *

app = Flask(__name__)
api = Api(app)

#Adding the user to the DB
api.add_resource(UserNamePath,"/user/<string:name>")

api.add_resource(Register, "/register")

api.add_resource(sign_in, "/sign_in")

app.run(debug=True, host= 'localhost')
