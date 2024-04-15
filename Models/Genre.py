from application import db


class Genre(db.Models):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    genre_name = db.Column(db.String, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'genre_name': self.genre_name
        }