from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
import psycopg2
from paths import *

app = Flask(__name__)
api = Api(app)

api.add_resource(UserInfo, "/userInfo/")

api.add_resource(UserNamePath,"/user/<string:name>")

app.run(debug=True, host= 'localhost')
