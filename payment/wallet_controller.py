from flask import Response, jsonify, request
from flask_restful import Resource
from jsonschema.exceptions import ValidationError

from application import app
from models import ProblemDetails
from payment import WalletDuplicateError, WalletService, WalletValidator

_wallet_service = WalletService()
_wallet_validator = WalletValidator()


class WalletController(Resource):
    @staticmethod
    @app.route("/api/v1/wallets", methods=["GET"])
    def get_wallets():
        return {"wallets": _wallet_service.find_all_wallets()}

    @staticmethod
    @app.route("/api/v1/purchase_manga", methods=["PUT"])
    def purchase_manga():

        try:
            request_data = request.get_json()
            _wallet_validator.validate_purchase_manga(request_data)
            return _wallet_service.purchase_manga(request_data)
        except ValidationError as ex:
            problem_details = ProblemDetails(
                type="Ошибка валидации в сущности Wallet",
                detail="Неверный формат данных",
                title=ex.message,
                status=400,
                instance="http://127.0.0.1/api/v1/purchase_manga"
            )
            return jsonify(problem_details), 400

    @staticmethod
    @app.route("/api/v1/wallets", methods=["POST"])
    def add_wallet():
        try:
            request_data = request.get_json()
            _wallet_validator.validate_add_wallet(request_data)
            _wallet_service.add_wallet(request_data)

            return {"wallets": _wallet_service.find_all_wallets()}
        except WalletDuplicateError as ex:
            return Response(ex.msg, status=409)
        except ValidationError as ex:
            problem_details = ProblemDetails(
                type="Ошибка валидации в сущности Wallet",
                detail="Неверный формат данных",
                title=ex.message,
                status=400,
                instance="http://127.0.0.1/api/v1/wallets"
            )
            return jsonify(problem_details), 400
        except Exception as ex:
            return Response(f"Непредвиденная ошибка: {ex}", status=500)