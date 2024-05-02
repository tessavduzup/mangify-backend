from application import db


class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    card_number = db.Column(db.String, nullable=True)
    money_amount = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'card_number': self.card_number,
            'money_amount': self.money_amount
        }