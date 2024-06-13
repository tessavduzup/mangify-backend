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


class UnnecessaryControllers:
    @staticmethod
    @app.route("/api/v1/fill_up_users_table", methods=["POST"])
    def fill_up_users_table():
        request_data = request.get_json()
        _user_service.fill_up_users_table(request_data)

        return _user_service.find_all_users()

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
    @app.route("/api/v1/users", methods=["DELETE"])
    def delete_all_users():
        _user_service.delete_all_users()
        return _user_service.find_all_users()