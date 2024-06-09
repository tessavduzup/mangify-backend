from flask import Response, jsonify, request
from flask_restful import Resource
from jsonschema.exceptions import ValidationError

from application import app
from exceptions import MangaDuplicateError, MangaNotFoundError
from loggers import manga_logger
from models import ProblemDetails
from services import MangaService
from validators import MangaValidator

_manga_service = MangaService()
_manga_validator = MangaValidator()


class MangaController(Resource):
    @staticmethod
    @app.route("/api/v1/manga", methods=["GET"])
    def get_all_manga():
        """Обработчик запроса, отображающий список всей манги в JSON-формате"""
        return _manga_service.find_all_manga()

    @staticmethod
    @app.route("/api/v1/top_manga", methods=["GET"])
    def get_top_manga():
        """Обработчик запроса, отображающий список популярной манги в JSON-формате"""
        return _manga_service.find_top_manga()

    @staticmethod
    @app.route("/api/v1/similar_manga/<int:manga_id>", methods=["GET"])
    def get_similar_manga(manga_id):
        """Обработчик запроса, отображающий список схожей манги в JSON-формате"""
        try:
            response = []
            similar_manga = _manga_service.find_similar_manga(manga_id)
            for manga in similar_manga:
                if manga.id != manga_id:
                    response.append(manga.to_dict())

            return response
        except MangaNotFoundError as ex:
            manga_logger.error("MangaNotFoundError")

            return Response(ex.msg, status=404)

    @staticmethod
    @app.route("/api/v1/manga/<int:manga_id>", methods=["GET"])
    def get_manga_by_id(manga_id):
        """Обработчик запроса, отображающий выбранную мангу в JSON-формате"""
        try:
            return _manga_service.find_manga(manga_id)
        except MangaNotFoundError as ex:
            manga_logger.error("MangaNotFoundError")

            return Response(ex.msg, status=404)
        except Exception as ex:
            manga_logger.error("Unknown Error")

            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/manga", methods=["POST"])
    def add_manga():
        """Обработчик запроса для добавления новой манги"""
        try:
            request_data = request.get_json()
            _manga_validator.validate_add_manga(request_data)
            _manga_service.add_manga(request_data)

            return _manga_service.find_all_manga()
        except MangaDuplicateError as ex:
            manga_logger.error("MangaDuplicateError")

            return Response(ex.msg, status=404)
        except ValidationError as ex:
            problem_details = ProblemDetails(
                type="Ошибка валидации в сущности Manga",
                detail="Неверный формат данных",
                title=ex.message,
                status=400,
                instance="http://127.0.0.1/api/v1/manga"
            )
            manga_logger.error("ValidationError")

            return jsonify(problem_details), 400
        except Exception as ex:
            manga_logger.error("Unknown Error")

            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/manga/<int:manga_id>", methods=["PUT"])
    def edit_manga(manga_id):
        """Обработчик запроса для редактирования манги"""
        try:
            request_data = request.get_json()
            _manga_validator.validate_edit_manga(request_data)
            _manga_service.update_manga(manga_id, request_data)

            return _manga_service.find_manga(manga_id)
        except MangaNotFoundError as ex:
            manga_logger.error("MangaNotFoundError")

            return Response(ex.msg, status=404)
        except ValidationError as ex:
            problem_details = ProblemDetails(
                type="Ошибка валидации в сущности User",
                detail="Неверный формат данных",
                title=ex.message,
                status=400,
                instance=f"http://127.0.0.1/api/v1/manga/{manga_id}"
            )
            manga_logger.error("ValidationError")

            return jsonify(problem_details), 400
        except Exception as ex:
            manga_logger.error("Unknown Error")

            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/manga/<int:manga_id>", methods=["DELETE"])
    def delete_manga(manga_id):
        """Обработчик запроса для удаления манги по ID"""
        try:
            _manga_service.delete_manga(manga_id)
            return manga_id
        except MangaNotFoundError as ex:
            manga_logger.error("MangaNotFoundError")

            return Response(ex.msg, status=404)
        except Exception as ex:
            manga_logger.error("Unknown Error")

            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/manga", methods=["DELETE"])
    def delete_all_manga():
        _manga_service.delete_all_manga()
        return _manga_service.find_all_manga()

    @staticmethod
    @app.route("/api/v1/fill_up_manga_table", methods=["POST"])
    def fill_up_manga_table():
        request_data = request.get_json()
        _manga_service.fill_up_manga_table(request_data)

        return _manga_service.find_all_manga()
