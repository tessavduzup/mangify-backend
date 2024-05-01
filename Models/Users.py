from Models.Manga import Manga
from Models.UserManga import UserManga
from application import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=True, unique=True)
    psw = db.Column(db.String, nullable=True)
    user_manga_fk = db.Column(db.Integer, db.ForeignKey('user_manga.id'), nullable=True)
    is_admin = db.Column(db.Boolean, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'cart': self.get_cart(self.id),
            'favourite_manga': self.get_favourite_manga(self.id),
            'purchased_manga': self.get_purchased_manga(self.id),
            'is_admin': self.is_admin
        }

    def get_cart(self, user_id):
        user_manga = UserManga.query.filter_by(id=user_id).first()
        if user_manga:
            manga_ids = user_manga.cart
            manga_in_cart = Manga.query.filter(Manga.id.in_(manga_ids)).all()
            return [manga.to_dict_for_cart() for manga in manga_in_cart]

        return []

    def get_favourite_manga(self, user_id):
        user_manga = UserManga.query.filter_by(id=user_id).first()
        if user_manga:
            manga_ids = user_manga.favourite_manga
            favourite_manga = Manga.query.filter(Manga.id.in_(manga_ids)).all()
            return [manga.to_dict() for manga in favourite_manga]

        return []

    def get_purchased_manga(self, user_id):
        user_manga = UserManga.query.filter_by(id=user_id).first()
        if user_manga:
            manga_ids = user_manga.purchased_manga
            purchased_manga = Manga.query.filter(Manga.id.in_(manga_ids)).all()
            return [manga.to_dict() for manga in purchased_manga]

        return []
