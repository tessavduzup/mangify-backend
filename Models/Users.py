from application import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=True)
    psw = db.Column(db.String, nullable=True)
    is_admin = db.Column(db.Boolean, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
        }