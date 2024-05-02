from application import db
from sqlalchemy.dialects.postgresql import ARRAY


class UserManga(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cart = db.Column(ARRAY(db.Integer), default=[])
    favourite_manga = db.Column(ARRAY(db.Integer), default=[])
    purchased_manga = db.Column(ARRAY(db.Integer), default=[])
