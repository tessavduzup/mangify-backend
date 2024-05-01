from flask import jsonify, request
from flask_restful import Resource
from application import app
from Services.user_service import UserService


_user_service = UserService()


class UserController(Resource):
    """Класс обработчиков запроса для работы с таблицей пользователей"""

    @staticmethod
    @app.route("/auth", methods=["POST"])
    def auth():
        request_data = request.get_json()
        return _user_service.auth(request_data)

    @staticmethod
    @app.route("/api/v1/users", methods=["GET"])
    def get_users():
        """Отображает список всех пользователей в JSON-формате"""
        return jsonify({"users": _user_service.find_all_users()})

    @staticmethod
    @app.route("/api/v1/users/<int:user_id>", methods=["GET"])
    def get_user(user_id):
        """Отображает выбранного пользователя в JSON-формате"""
        return jsonify(_user_service.find_user(user_id))

    @staticmethod
    @app.route("/api/v1/users", methods=["POST"])
    def add_user():
        """Добавляет нового пользователя"""
        request_data = request.get_json()
        _user_service.add_user(request_data)

        return jsonify({"users": _user_service.find_all_users()})

    @staticmethod
    @app.route("/api/v1/users/<int:user_id>", methods=["PUT"])
    def edit_user(user_id):
        """Редактирует информацию о пользователе"""
        request_data = request.get_json()
        _user_service.update_user(user_id, request_data)

        return jsonify(_user_service.find_user(user_id))

    @staticmethod
    @app.route("/api/v1/users/<int:user_id>", methods=["DELETE"])
    def delete_user(user_id):
        """Удаляет пользователя"""
        _user_service.delete_user(user_id)
        return jsonify(user_id)

    @staticmethod
    @app.route("/api/v1/delete_all_users", methods=["DELETE"])
    def delete_all_users():
        _user_service.delete_all_users()
        return jsonify({"all_manga": _user_service.find_all_users()})

    @staticmethod
    @app.route("/api/v1/fill_up_users_table", methods=["POST"])
    def fill_up_users_table():
        request_data = request.get_json()
        _user_service.fill_up_users_table(request_data)

        return jsonify({"all_manga": _user_service.find_all_users()})

    # @staticmethod
    # @app.route("/api/v1/cart/<int:user_id>", methods=["GET"])
    # def get_cart(user_id):
    #     return jsonify({"cart": _user_service.get_cart(user_id)})
    #
    # @staticmethod
    # @app.route("/api/v1/favourite_manga/<int:user_id>", methods=["GET"])
    # def get_favourite_manga(user_id):
    #     return jsonify({"favourite_manga": _user_service.get_favourite_manga(user_id)})
    #
    # @staticmethod
    # @app.route("/api/v1/purchased_manga/<int:user_id>", methods=["GET"])
    # def get_purchased_manga(user_id):
    #     return jsonify({"purchased_manga": _user_service.get_purchased_manga(user_id)})
