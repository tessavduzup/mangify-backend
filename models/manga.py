from models import Image
from application import db


class Manga(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=True)
    title_en = db.Column(db.String, nullable=True)
    author = db.Column(db.String, nullable=True)
    wrap_fk = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=True)
    description = db.Column(db.Text, nullable=True)
    genre = db.Column(db.JSON, nullable=True)
    price = db.Column(db.Integer, nullable=True)

    @staticmethod
    def get_path_to_file(wrap_id):
        file = db.session.query(Image).join(Manga).filter_by(id=wrap_id).first()
        if file:
            return file.wrap_path
        else:
            return None

    def to_dict(self):
        return {
            'id': self.id,
            'author': self.author,
            'title': self.title,
            'title-en': self.title_en,
            'wrap_path': self.get_path_to_file(self.wrap_fk),
            'description': self.description,
            'genre': self.genre,
            'price': self.price
        }

    def to_dict_for_cart(self):
        return {
            'id': self.id,
            'title': self.title,
            'title-en': self.title_en,
            'wrap_path': self.get_path_to_file(self.wrap_fk),
            'price': self.price
        }
