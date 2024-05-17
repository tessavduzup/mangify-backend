from flask import jsonify, request, Response
from flask_restful import Resource

from exceptions import UserNotFoundError, UsernameDuplicateError, MangaDuplicateError, MangaNotFoundError
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
        try:
            return jsonify(_user_service.find_user(user_id))
        except UserNotFoundError as ex:
            return Response(ex.msg, status=404)
        except Exception as ex:
            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/users", methods=["POST"])
    def add_user():
        """Добавляет нового пользователя"""
        try:
            request_data = request.get_json()
            _user_service.add_user(request_data)

            return jsonify({"users": _user_service.find_all_users()})
        except UsernameDuplicateError as ex:
            return Response(ex.msg, status=409)
        except Exception as ex:
            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/users/<int:user_id>", methods=["PUT"])
    def edit_user(user_id):
        """Редактирует информацию о пользователе"""
        try:
            request_data = request.get_json()
            _user_service.update_user(user_id, request_data)

            return jsonify(_user_service.find_user(user_id))
        except UserNotFoundError as ex:
            return Response(ex.msg, status=404)
        except Exception as ex:
            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/users/<int:user_id>", methods=["DELETE"])
    def delete_user(user_id):
        """Удаляет пользователя"""
        try:
            _user_service.delete_user(user_id)
            return jsonify(user_id)
        except UserNotFoundError as ex:
            return Response(ex.msg, status=404)
        except Exception as ex:
            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/users/<int:user_id>/add_to_cart", methods=["POST"])
    def add_to_cart(user_id):
        try:
            request_data = request.get_json()
            manga_id = request_data['manga_id']
            _user_service.add_to_cart(user_id, manga_id)

            return jsonify(_user_service.find_user(user_id))
        except MangaDuplicateError as ex:
            return Response(ex.msg, status=409)
        except Exception as ex:
            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/users/<int:user_id>/delete_from_cart", methods=["DELETE"])
    def delete_from_cart(user_id):
        try:
            request_data = request.get_json()
            manga_id = request_data['manga_id']
            _user_service.delete_from_cart(user_id, manga_id)

            return jsonify(_user_service.find_user(user_id))
        except MangaNotFoundError as ex:
            return Response(ex.msg, status=404)
        except Exception as ex:
            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/users/<int:user_id>/add_to_favourite_manga", methods=["POST"])
    def add_to_favourite(user_id):
        try:
            request_data = request.get_json()
            manga_id = request_data['manga_id']
            _user_service.add_to_favourite(user_id, manga_id)

            return jsonify(_user_service.find_user(user_id))
        except MangaDuplicateError as ex:
            return Response(ex.msg, status=409)
        except Exception as ex:
            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/users/<int:user_id>/delete_from_favourite_manga", methods=["DELETE"])
    def delete_from_favourite(user_id):
        try:
            request_data = request.get_json()
            manga_id = request_data['manga_id']
            _user_service.delete_from_favourite(user_id, manga_id)

            return jsonify(_user_service.find_user(user_id))
        except MangaNotFoundError as ex:
            return Response(ex.msg, status=404)
        except Exception as ex:
            return Response(f"Непредвиденная ошибка: {ex}", status=500)

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
    # @app.route("/api/v1/user/<int:user_id>/cart", methods=["GET"])
    # def get_cart(user_id):
    #     return jsonify({"cart": _user_service.get_cart(user_id)})
    #
    # @staticmethod
    # @app.route("/api/v1/user/<int:user_id>/favourite_manga", methods=["GET"])
    # def get_favourite_manga(user_id):
    #     return jsonify({"favourite_manga": _user_service.get_favourite_manga(user_id)})
    #
    # @staticmethod
    # @app.route("/api/v1/user/<int:user_id>/purchased_manga", methods=["GET"])
    # def get_purchased_manga(user_id):
    #     return jsonify({"purchased_manga": _user_service.get_purchased_manga(user_id)})
