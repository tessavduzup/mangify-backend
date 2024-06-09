import datetime

from application import db
from models import Orders, UserManga, Users
from payment import Wallet, WalletDuplicateError
from utils.email_utils import send_cheque


class WalletService:
    def purchase_manga(self, request_data):
        usermanga = db.session.query(UserManga).join(Users).filter_by(id=request_data['user_id']).first()
        wallet = Wallet.query.filter_by(card_number=request_data['card_number']).first()

        if wallet.money_amount < request_data['amount_of_buying']:
            return {"error": "No money - no honey"}
        else:
            wallet.money_amount -= request_data['amount_of_buying']
            db.session.flush()

            usermanga.purchased_manga = usermanga.cart
            usermanga.cart = []
            db.session.flush()

            order_code = f"WEB-ORDER-{request_data['user_id']}{request_data['amount_of_buying']}"
            new_order = Orders(order_code=order_code, order_sum=request_data['amount_of_buying'],
                               client=request_data['user_id'], buying_content={"buying_content": request_data['goods']})

            db.session.add(new_order)
            db.session.commit()

            send_cheque(usermanga.email, order_code, request_data['amount_of_buying'],
                        request_data['card_number'][-4:], request_data['goods'],
                        datetime.datetime.now().replace(microsecond=0))

            return {"success": "Оплата прошла успешно"}

    def find_all_wallets(self):
        wallets = []
        raw_wallets = Wallet.query.all()
        for row in raw_wallets:
            wallet = row.to_dict()
            wallets.append(wallet)

        return wallets

    def add_wallet(self, request_data):
        wallet_check = Wallet.query.filter_by(card_number=request_data['card_number']).first()
        if wallet_check:
            raise WalletDuplicateError("Кошелёк с такой картой уже существует")

        new_wallet = Wallet(card_number=request_data['card_number'], money_amount=request_data['money_amount'])
        db.session.add(new_wallet)
        db.session.commit()