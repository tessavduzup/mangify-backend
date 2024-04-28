from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

# Для работы кириллицы
app.json.ensure_ascii = False
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///mangify.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
UPLOAD_FOLDER = 'images'
