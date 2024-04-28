from Models.Image import Image
from application import db


class Manga(db.Model): # TODO
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=True)
    # title_en = db.Column(db.String, nullable=True)
    author = db.Column(db.String, nullable=True)
    wrap_fk = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=True)
    description = db.Column(db.Text, nullable=True)
    genre = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=True)
    price = db.Column(db.Integer, nullable=True)

    @staticmethod
    def get_path_to_file(wrap_id):
        file = db.session.query(Image).join(Manga).filter_by(id=wrap_id).first()
        if file:
            return file.path_to_file
        else:
            return None

    def to_dict(self):
        return {
            'id': self.id,
            'author': self.author,
            'title': self.title,
            'wrap': self.get_path_to_file(self.wrap_fk),
            'description': self.description,
            'genre_id': self.genre,
            'price': self.price
        }
