from flask_restful import Api, Resource, reqparse
from dbFunctions import *
import json


class UserNamePath(Resource):

    def get(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("username")
        parser.add_argument("password")
        jsonData = executeQuery('''Select * from users where username = \'''' + name + '\'')
        return jsonData, 200

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("username")
        parser.add_argument("password")

        args = parser.parse_args()

        insert('''INSERT INTO users (username,password) VALUES(\'''' + str(args["username"]) + '''\',\'''' + str(
            args["password"]) + '''\')''')

        return 200
