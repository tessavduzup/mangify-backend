from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api()


class UserController:

    @app.route("/")
    def home(self):
        pass

    @app.route("/profile/<id>")
    def my_account(self):
        pass

    @app.route("/manga/<id>")
    def selected_manga(self):
        pass
