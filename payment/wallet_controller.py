from flask import jsonify, request, Response
from flask_restful import Resource
from application import app
from payment import WalletService, WalletDuplicateError


_wallet_service = WalletService()


class WalletController(Resource):
    @staticmethod
    @app.route("/api/v1/wallets", methods=["GET"])
    def get_wallets():
        return jsonify({"wallets": _wallet_service.find_all_wallets()})

    @staticmethod
    @app.route("/api/v1/purchase_manga", methods=["PUT"])
    def purchase_manga():
        request_data = request.get_json()

        return _wallet_service.purchase_manga(request_data)

    @staticmethod
    @app.route("/api/v1/wallets", methods=["POST"])
    def add_wallet():
        try:
            request_data = request.get_json()
            _wallet_service.add_wallet(request_data)

            return jsonify({"wallets": _wallet_service.find_all_wallets()})
        except WalletDuplicateError as ex:
            return Response(ex.msg, status=409)
        except Exception as ex:
            return Response(f"Непредвиденная ошибка: {ex}", status=500)
