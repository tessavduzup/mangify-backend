from application import db


class UserManga(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cart = db.Column(db.JSON, default={"cart": []})
    favorite_manga = db.Column(db.JSON, default={"favorite_manga": []})
    purchased_manga = db.Column(db.JSON, default={"purchased_manga": []})