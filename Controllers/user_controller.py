from flask import jsonify, request
from flask_restful import Resource
from application import app
from Services.user_service import UserService


_user_service = UserService()


class UserController(Resource):
    """Класс обработчиков запроса для работы с таблицей пользователей"""

    @staticmethod
    @app.route("/v1/users", methods=["GET"])
    def get_users():
        """Отображает список всех пользователей в JSON-формате"""
        return jsonify({"users": _user_service.find_all_users()})

    @staticmethod
    @app.route("/v1/users/<int:user_id>", methods=["GET"])
    def get_user(user_id):
        """Отображает выбранного пользователя в JSON-формате"""
        return jsonify(_user_service.find_user(user_id))

    @staticmethod
    @app.route("/v1/users", methods=["POST"])
    def add_user():
        """Добавляет нового пользователя"""
        request_data = request.get_json()
        _user_service.add_user(request_data)

        return jsonify({"genres": _user_service.find_all_users()})

    @staticmethod
    @app.route("/v1/users/<int:user_id>", methods=["PUT"])
    def edit_user(user_id):
        """Редактирует информацию о пользователе"""
        request_data = request.get_json()
        _user_service.update_user(user_id, request_data)

        return jsonify(_user_service.find_user(user_id))

    @staticmethod
    @app.route("/v1/users/<int:user_id>", methods=["DELETE"])
    def delete_user(user_id):
        """Удаляет пользователя"""
        _user_service.delete_user(user_id)
        return jsonify(user_id)
