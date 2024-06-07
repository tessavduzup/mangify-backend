from application import db


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_code = db.Column(db.String, nullable=True)
    order_sum = db.Column(db.Integer, nullable=True)
    client = db.Column(db.Integer,db.ForeignKey("users.id"), nullable=True)
    buying_content = db.Column(db.JSON, nullable=True)
