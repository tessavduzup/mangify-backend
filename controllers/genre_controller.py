from flask import jsonify, request, Response
from flask_restful import Resource

from exceptions import GenreNotFoundError, GenreDuplicateError
from application import app
from services.genre_service import GenreService


_genre_service = GenreService()


class GenreController(Resource):
    @staticmethod
    @app.route("/api/v1/manga/genres", methods=["GET"])
    def get_genres():
        """Обработчик запроса, отображающий список всех жанров в JSON-формате"""
        return jsonify({"genres": _genre_service.find_all_genres()})

    @staticmethod
    @app.route("/api/v1/manga/genres/<int:genre_id>", methods=["GET"])
    def get_genre(genre_id):
        """Обработчик запроса, отображающий выбранный жанр в JSON-формате"""
        try:
            return jsonify(_genre_service.find_genre(genre_id))
        except GenreNotFoundError as ex:
            return Response(ex.msg, status=404)
        except Exception as ex:
            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/manga/genres", methods=["POST"])
    def add_genre():
        """Обработчик запроса для добавления нового жанра"""
        try:
            request_data = request.get_json()
            _genre_service.add_genre(request_data)

            return jsonify({"genres": _genre_service.find_all_genres()})
        except GenreDuplicateError as ex:
            return Response(ex.msg, status=409)
        except Exception as ex:
            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/manga/genres/<int:genre_id>", methods=["PUT"])
    def edit_genre(genre_id):
        """Обработчик запроса для редактирования жанра"""
        try:
            request_data = request.get_json()
            _genre_service.update_genre(genre_id, request_data)

            return jsonify(_genre_service.find_genre(genre_id))
        except GenreNotFoundError as ex:
            return Response(ex.msg, status=404)
        except Exception as ex:
            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/manga/genres/<int:genre_id>", methods=["DELETE"])
    def delete_genre(genre_id):
        """Обработчик запроса для удаления категории по ID"""
        try:
            _genre_service.delete_genre(genre_id)
            return jsonify(genre_id)
        except GenreNotFoundError as ex:
            return Response(ex.msg, status=404)
        except Exception as ex:
            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/delete_all_genres", methods=["DELETE"])
    def delete_all_genres():
        _genre_service.delete_all_genres()
        return jsonify({"genres": _genre_service.find_all_genres()})

    @staticmethod
    @app.route("/api/v1/fill_up_genres_table", methods=["POST"])
    def fill_up_genres_table():
        request_data = request.get_json()
        _genre_service.fill_up_genres_table(request_data)

        return jsonify({"genres": _genre_service.find_all_genres()})