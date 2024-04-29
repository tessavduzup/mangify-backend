from flask import jsonify, request
from flask_restful import Resource
from application import app
from Services.genre_service import GenreService


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
        return jsonify(_genre_service.find_genre(genre_id))

    @staticmethod
    @app.route("/api/v1/manga/genres", methods=["POST"])
    def add_genre():
        """Обработчик запроса для добавления нового жанра"""
        request_data = request.get_json()
        _genre_service.add_genre(request_data)

        return jsonify({"genres": _genre_service.find_all_genres()})

    @staticmethod
    @app.route("/api/v1/manga/genres/<int:genre_id>", methods=["PUT"])
    def edit_genre(genre_id):
        """Обработчик запроса для редактирования жанра"""
        request_data = request.get_json()
        _genre_service.update_genre(genre_id, request_data)

        return jsonify(_genre_service.find_genre(genre_id))

    @staticmethod
    @app.route("/api/v1/manga/genres/<int:genre_id>", methods=["DELETE"])
    def delete_genre(genre_id):
        """Обработчик запроса для удаления категории по ID"""
        _genre_service.delete_genre(genre_id)
        return jsonify(genre_id)