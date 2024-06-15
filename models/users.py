from application import db
from models import UserManga


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=True, unique=True)
    email = db.Column(db.String, nullable=True, unique=True)
    psw = db.Column(db.String, nullable=True)
    user_manga_fk = db.Column(db.Integer, db.ForeignKey('user_manga.id'), nullable=True)
    is_admin = db.Column(db.Boolean, nullable=True)

    def to_dict(self):
        user_manga = UserManga.query.filter_by(id=self.user_manga_fk).first()
        return {
            'id': self.id,
            'username': self.username,
            "email": self.email,
            'cart': user_manga.cart["cart"],
            'favorite_manga': user_manga.favorite_manga["favorite_manga"],
            'purchased_manga': user_manga.purchased_manga["purchased_manga"],
            'is_admin': self.is_admin
        }
