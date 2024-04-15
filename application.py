from flask import Flask
from flask_restful import Api
from venv.config import host, user, password, db_name
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

# Для работы кириллицы
app.json.ensure_ascii = False
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
