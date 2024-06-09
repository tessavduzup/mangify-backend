from flask import Response, jsonify, request
from flask_restful import Resource
from jsonschema.exceptions import ValidationError

from application import app
from exceptions import GenreDuplicateError, GenreNotFoundError
from loggers import genre_logger
from models import ProblemDetails
from services import GenreService
from validators import GenreValidator

_genre_service = GenreService()
_genre_validator = GenreValidator()


class GenreController(Resource):
    @staticmethod
    @app.route("/api/v1/manga/genres", methods=["GET"])
    def get_genres():
        """Обработчик запроса, отображающий список всех жанров в JSON-формате"""
        return _genre_service.find_all_genres()

    @staticmethod
    @app.route("/api/v1/manga/genres/<int:genre_id>", methods=["GET"])
    def get_genre(genre_id):
        """Обработчик запроса, отображающий выбранный жанр в JSON-формате"""
        try:
            return _genre_service.find_genre(genre_id)
        except GenreNotFoundError as ex:
            problem_details = ProblemDetails(
                type="Ошибка в сущности Genre",
                detail="Жанр не найден",
                title=ex.msg,
                status=404,
                instance="http://127.0.0.1/api/v1/purchase_manga"
            )
            genre_logger.error("GenreNotFoundError")

            return jsonify(problem_details), 404
        except Exception as ex:
            problem_details = ProblemDetails(
                type="Ошибка в сущности Genre",
                detail="Непредвиденная ошибка",
                title=f"{ex}",
                status=500,
                instance="http://127.0.0.1/api/v1/purchase_manga"
            )
            genre_logger.error("Unknown Error")

            return jsonify(problem_details), 500

    @staticmethod
    @app.route("/api/v1/manga/genres", methods=["POST"])
    def add_genre():
        """Обработчик запроса для добавления нового жанра"""
        try:
            request_data = request.get_json()
            _genre_validator.validate_add_genre(request_data)
            _genre_service.add_genre(request_data)

            return _genre_service.find_all_genres()
        except GenreDuplicateError as ex:
            genre_logger.error("GenreDuplicateError")

            return Response(ex.msg, status=409)
        except ValidationError as ex:
            problem_details = ProblemDetails(
                type="Ошибка валидации в сущности Genre",
                detail="Неверный формат данных",
                title=ex.message,
                status=400,
                instance="http://127.0.0.1/api/v1/manga/genres"
            )
            genre_logger.error("ValidationError")

            return jsonify(problem_details), 400
        except Exception as ex:
            genre_logger.error("Unknown Error")

            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/manga/genres/<int:genre_id>", methods=["PUT"])
    def edit_genre(genre_id):
        """Обработчик запроса для редактирования жанра"""
        try:
            request_data = request.get_json()
            _genre_validator.validate_edit_genre(request_data)
            _genre_service.update_genre(genre_id, request_data)

            return _genre_service.find_genre(genre_id)
        except GenreNotFoundError as ex:
            genre_logger.error("GenreNotFoundError")

            return Response(ex.msg, status=404)
        except ValidationError as ex:
            problem_details = ProblemDetails(
                type="Ошибка валидации в сущности Genre",
                detail="Неверный формат данных",
                title=ex.message,
                status=400,
                instance=f"http://127.0.0.1/api/v1/manga/genres/{genre_id}"
            )
            genre_logger.error("ValidationError")

            return jsonify(problem_details), 400
        except Exception as ex:
            genre_logger.error("Unknown Error")

            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/manga/genres/<int:genre_id>", methods=["DELETE"])
    def delete_genre(genre_id):
        """Обработчик запроса для удаления категории по ID"""
        try:
            _genre_service.delete_genre(genre_id)
            return genre_id
        except GenreNotFoundError as ex:
            genre_logger.error("GenreNotFoundError")

            return Response(ex.msg, status=404)
        except Exception as ex:
            genre_logger.error("Unknown Error")

            return Response(f"Непредвиденная ошибка: {ex}", status=500)

    @staticmethod
    @app.route("/api/v1/genres", methods=["DELETE"])
    def delete_all_genres():
        _genre_service.delete_all_genres()
        return _genre_service.find_all_genres()

    @staticmethod
    @app.route("/api/v1/fill_up_genres_table", methods=["POST"])
    def fill_up_genres_table():
        request_data = request.get_json()
        _genre_service.fill_up_genres_table(request_data)

        return _genre_service.find_all_genres()