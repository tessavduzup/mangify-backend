from flask import jsonify
from Payment.Models.Wallet import Wallet
from Models.Users import Users
from Models.UserManga import UserManga
from application import db


class WalletService:
    def purchase_manga(self, request_data):
        usermanga = db.session.query(UserManga).join(Users).filter_by(id=request_data['user_id']).first()
        wallet = Wallet.query.filter_by(card_number=request_data['card_number']).first()

        if wallet.money_amount < request_data['amount_of_buying']:
            return jsonify({"error": "Недостаточно средств на карте"})
        else:
            wallet.money_amount -= request_data['amount_of_buying']
            db.session.flush()

            usermanga.purchased_manga = usermanga.cart
            usermanga.cart = []
            db.session.commit()
            return jsonify({"success": "Оплата прошла успешно"})

    def find_all_wallets(self):
        wallets = []
        raw_wallets = Wallet.query.all()
        for row in raw_wallets:
            wallet = row.to_dict()
            wallets.append(wallet)

        return wallets

    def add_wallet(self, request_data):
        new_wallet = Wallet(card_number=request_data['card_number'], money_amount=request_data['money_amount'])
        db.session.add(new_wallet)
        db.session.commit()