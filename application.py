import redis
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask("Mangify-Backend")
api = Api(app)
CORS(app)

app.json.ensure_ascii = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mangify.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
redis_client = redis.StrictRedis(host="localhost", port=6379, charset="utf-8", decode_responses=True)
