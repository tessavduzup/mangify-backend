from application import db


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path_to_file = db.Column(db.String, nullable=True)
