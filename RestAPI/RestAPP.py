from flask import Flask
from flask_restful import Api
from paths import *

app = Flask(__name__)
api = Api(app)

api.add_resource(UserInfo, "/userInfo/")

api.add_resource(UserNamePath, "/user/<string:name>")

app.run(debug=True, host='localhost')
