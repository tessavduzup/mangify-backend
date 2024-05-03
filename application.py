from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
CORS(app, supports_credentials=True, expose_headers="Content-Type", allow_headers="Content-Type")

app.json.ensure_ascii = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mangify.db'	
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
