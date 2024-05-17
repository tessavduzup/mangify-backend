from application import db


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wrap_path = db.Column(db.String, nullable=True)
