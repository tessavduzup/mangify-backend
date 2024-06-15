from application import db


class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    card_number = db.Column(db.String, nullable=True)
    card_date = db.Column(db.String, nullable=True)
    cvv = db.Column(db.String, nullable=True)
    money_amount = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'card_number': self.card_number,
            'card_date': self.card_date,
            'cvv': self.cvv,
            'money_amount': self.money_amount
        }
