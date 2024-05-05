from application import db


class UserManga(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cart = db.Column(db.JSON, default={"cart": []})
    favourite_manga = db.Column(db.JSON, default={"favourite_manga": []})
    purchased_manga = db.Column(db.JSON, default={"purchased_manga": []})