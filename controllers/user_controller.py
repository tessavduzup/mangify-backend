from flask import Response, jsonify, request
from flask_restful import Resource
from jsonschema.exceptions import ValidationError

from application import app
from exceptions import (EmailDuplicateError, MangaDuplicateError,
                        MangaNotFoundError, UsernameDuplicateError,
                        UserNotFoundError)
from loggers import users_logger
from models import ProblemDetails
from services import UserService
from validators import UserValidator

_user_service = UserService()
_user_validator = UserValidator()


class UserController(Resource):
    """Класс обработчиков запроса для работы с таблицей пользователей"""

    @staticmethod
    @app.route("/auth", methods=["POST"])
    def auth():
        request_data = request.get_json()
        return _user_service.auth(request_data)

    @staticmethod
    @app.route("/confirm_email", methods=["POST"])
    def email_confirmation():
        request_data = request.get_json()
        return _user_service.email_confirmation(request_data)

    @staticmethod
    @app.route("/api/v1/users", methods=["GET"])
    def get_users():
        """Отображает список всех пользователей в JSON-формате"""
        return _user_service.find_all_users()

    @staticmethod
    @app.route("/api/v1/users/<int:user_id>", methods=["GET"])
    def get_user(user_id):
        """Отображает выбранного пользователя в JSON-формате"""
        try:
            return jsonify(_user_service.find_user(user_id))
        except UserNotFoundError as ex:
            users_logger.error("UserNotFoundError")

            return Response(ex.msg, status=404)
        except Exception as ex:
            users_logger.error("Unknown Error")

            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/users", methods=["POST"])
    def add_user():
        """Добавляет нового пользователя"""
        try:
            request_data = request.get_json()
            _user_validator.validate_add_user(request_data)
            _user_service.add_user(request_data)

            return _user_service.find_all_users()
        except UsernameDuplicateError as ex:
            users_logger.error("UsernameDuplicateError")

            return Response(ex.msg, status=409)
        except EmailDuplicateError as ex:
            users_logger.error("EmailDuplicateError")

            return Response(ex.msg, status=409)
        except ValidationError as ex:
            problem_details = ProblemDetails(
                type="Ошибка валидации в сущности User",
                detail="Неверный формат данных",
                title=ex.message,
                status=400,
                instance="http://127.0.0.1/api/v1/users"
            )
            users_logger.error("ValidationError")

            return jsonify(problem_details), 400
        except Exception as ex:
            users_logger.error("Unknown Error")

            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/users/<int:user_id>", methods=["PUT"])
    def edit_user(user_id):
        """Редактирует информацию о пользователе"""
        try:
            request_data = request.get_json()
            _user_validator.validate_edit_user(request_data)
            _user_service.update_user(user_id, request_data)

            return _user_service.find_user(user_id)
        except UserNotFoundError as ex:
            users_logger.error("UserNotFoundError")

            return Response(ex.msg, status=404)
        except ValidationError as ex:
            problem_details = ProblemDetails(
                type="Ошибка валидации в сущности User",
                detail="Неверный формат данных",
                title=ex.message,
                status=400,
                instance=f"http://127.0.0.1/api/v1/users/{user_id}"
            )
            users_logger.error("ValidationError")

            return jsonify(problem_details), 400
        except Exception as ex:
            users_logger.error("Unknown Error")

            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/users/<int:user_id>", methods=["DELETE"])
    def delete_user(user_id):
        """Удаляет пользователя"""
        try:
            _user_service.delete_user(user_id)
            return user_id
        except UserNotFoundError as ex:
            users_logger.error("UserNotFoundError")

            return Response(ex.msg, status=404)
        except Exception as ex:
            users_logger.error("Unknown Error")

            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/users/<int:user_id>/cart", methods=["POST"])
    def add_to_cart(user_id):
        try:
            request_data = request.get_json()
            manga_id = request_data['manga_id']
            _user_service.add_to_cart(user_id, manga_id)

            return _user_service.find_user(user_id)
        except MangaDuplicateError as ex:
            users_logger.error("MangaDuplicateError")

            return Response(ex.msg, status=409)
        except Exception as ex:
            users_logger.error("Unknown Error")

            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/users/<int:user_id>/cart", methods=["DELETE"])
    def delete_from_cart(user_id):
        try:
            request_data = request.get_json()
            manga_id = request_data['manga_id']
            _user_service.delete_from_cart(user_id, manga_id)

            return _user_service.find_user(user_id)
        except MangaNotFoundError as ex:
            users_logger.error("MangaNotFoundError")

            return Response(ex.msg, status=404)
        except Exception as ex:
            users_logger.error("Unknown Error")

            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/users/<int:user_id>/favorite", methods=["POST"])
    def add_to_favorite(user_id):
        try:
            request_data = request.get_json()
            manga_id = request_data['manga_id']
            _user_service.add_to_favorite(user_id, manga_id)

            return _user_service.find_user(user_id)
        except MangaDuplicateError as ex:
            users_logger.error("MangaDuplicateError")

            return Response(ex.msg, status=409)
        except Exception as ex:
            users_logger.error("Unknown Error")

            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/users/<int:user_id>/favorite", methods=["DELETE"])
    def delete_from_favorite(user_id):
        try:
            request_data = request.get_json()
            manga_id = request_data['manga_id']
            _user_service.delete_from_favorite(user_id, manga_id)

            return _user_service.find_user(user_id)
        except MangaNotFoundError as ex:
            users_logger.error("MangaNotFoundError")

            return Response(ex.msg, status=404)
        except Exception as ex:
            users_logger.error("Unknown Error")

            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/users", methods=["DELETE"])
    def delete_all_users():
        _user_service.delete_all_users()
        return _user_service.find_all_users()

    @staticmethod
    @app.route("/api/v1/fill_up_users_table", methods=["POST"])
    def fill_up_users_table():
        request_data = request.get_json()
        _user_service.fill_up_users_table(request_data)

        return _user_service.find_all_users()

    @staticmethod
    @app.route("/api/v1/users/<int:user_id>/cart", methods=["GET"])
    def get_cart(user_id):
        return _user_service.get_cart(user_id)

    @staticmethod
    @app.route("/api/v1/users/<int:user_id>/favorite", methods=["GET"])
    def get_favorite_manga(user_id):
        return _user_service.get_favorite_manga(user_id)

    @staticmethod
    @app.route("/api/v1/users/<int:user_id>/purchased", methods=["GET"])
    def get_purchased_manga(user_id):
        return _user_service.get_purchased_manga(user_id)

    @staticmethod
    @app.route("/api/v1/users/<int:user_id>/manga", methods=["GET"])
    def get_user_manga(user_id):
        return _user_service.get_user_manga(user_id)

    @staticmethod
    @app.route("/api/v1/users/<int:user_id>/top_manga", methods=["GET"])
    def get_user_top_manga(user_id):
        return _user_service.get_user_top_manga(user_id)
