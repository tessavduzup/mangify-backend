from flask import jsonify, request
from flask_restful import Resource
from application import app
from Services.manga_service import MangaService


_manga_service = MangaService()


class MangaController(Resource):
    @staticmethod
    @app.route("/v1/manga", methods=["GET"])
    def get_all_manga():
        """Обработчик запроса, отображающий список всей манги в JSON-формате"""
        return jsonify({"all_manga": _manga_service.find_all_manga()})

    @staticmethod
    @app.route("/v1/manga/<int:manga_id>", methods=["GET"])
    def get_manga_by_id(manga_id):
        """Обработчик запроса, отображающий выбранную мангу в JSON-формате"""
        return jsonify(_manga_service.find_manga(manga_id))

    @staticmethod
    @app.route("/v1/manga", methods=["POST"])
    def add_manga():
        """Обработчик запроса для добавления новой манги"""
        request_data = request.get_json()
        _manga_service.add_manga(request_data)

        return jsonify({"genres": _manga_service.find_all_manga()})

    @staticmethod
    @app.route("/v1/manga/<int:manga_id>", methods=["PUT"])
    def edit_mang(manga_id):
        """Обработчик запроса для редактирования манги"""
        request_data = request.get_json()
        _manga_service.update_manga(manga_id, request_data)

        return jsonify(_manga_service.find_manga(manga_id))

    @staticmethod
    @app.route("/v1/manga/<int:manga_id>", methods=["DELETE"])
    def delete_manga(manga_id):
        """Обработчик запроса для удаления манги по ID"""
        _manga_service.delete_manga(manga_id)
        return jsonify(manga_id)
