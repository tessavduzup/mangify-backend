from flask import jsonify, request, Response
from flask_restful import Resource

from exceptions import MangaNotFoundError, MangaDuplicateError
from application import app
from Services.manga_service import MangaService


_manga_service = MangaService()


class MangaController(Resource):
    @staticmethod
    @app.route("/api/v1/manga", methods=["GET"])
    def get_all_manga():
        """Обработчик запроса, отображающий список всей манги в JSON-формате"""
        return jsonify({"all_manga": _manga_service.find_all_manga()})

    @staticmethod
    @app.route("/api/v1/top_manga", methods=["GET"])
    def get_top_manga():
        """Обработчик запроса, отображающий список популярной манги в JSON-формате"""
        return jsonify({"top_manga": _manga_service.find_top_manga()})

    @staticmethod
    @app.route("/api/v1/manga/<int:manga_id>", methods=["GET"])
    def get_manga_by_id(manga_id):
        """Обработчик запроса, отображающий выбранную мангу в JSON-формате"""
        try:
            return jsonify(_manga_service.find_manga(manga_id))
        except MangaNotFoundError as ex:
            return Response(ex.msg, status=404)
        except Exception as ex:
            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/manga", methods=["POST"])
    def add_manga():
        """Обработчик запроса для добавления новой манги"""
        try:
            request_data = request.get_json()
            _manga_service.add_manga(request_data)

            return jsonify({"all_manga": _manga_service.find_all_manga()})
        except MangaDuplicateError as ex:
            return Response(ex.msg, status=404)
        except Exception as ex:
            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/manga/<int:manga_id>", methods=["PUT"])
    def edit_manga(manga_id):
        """Обработчик запроса для редактирования манги"""
        try:
            request_data = request.get_json()
            _manga_service.update_manga(manga_id, request_data)

            return jsonify(_manga_service.find_manga(manga_id))
        except MangaNotFoundError as ex:
            return Response(ex.msg, status=404)
        except Exception as ex:
            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/manga/<int:manga_id>", methods=["DELETE"])
    def delete_manga(manga_id):
        """Обработчик запроса для удаления манги по ID"""
        try:
            _manga_service.delete_manga(manga_id)
            return jsonify(manga_id)
        except MangaNotFoundError as ex:
            return Response(ex.msg, status=404)
        except Exception as ex:
            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/delete_all_manga", methods=["DELETE"])
    def delete_all_manga():
        _manga_service.delete_all_manga()
        return jsonify({"all_manga": _manga_service.find_all_manga()})

    @staticmethod
    @app.route("/api/v1/fill_up_manga_table", methods=["POST"])
    def fill_up_manga_table():
        request_data = request.get_json()
        _manga_service.fill_up_manga_table(request_data)

        return jsonify({"all_manga": _manga_service.find_all_manga()})
