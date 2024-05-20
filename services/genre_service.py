from exceptions import GenreNotFoundError, GenreDuplicateError
from models import Genre
from application import db


class GenreService:
    """Класс, описывающий работу с таблицей для жанров манги в БД"""

    def find_genre(self, genre_name):
        """Находит жанр по ID
        в БД и возвращает его в виде словаря"""
        genre = Genre.query.filter_by(genre_name=genre_name).first()
        if genre is None:
            raise GenreNotFoundError("Такой жанр не найден")

        return genre.to_dict()

    def find_all_genres(self):
        """Возвращает все жанры,
        находящиеся в БД"""
        genres = []
        raw_genres = Genre.query.all()
        for row in raw_genres:
            genre = row.to_dict()
            genres.append(genre)

        return genres

    def add_genre(self, request_data):
        """По данным запроса добавляет новый жанр в БД"""
        genre_check = Genre.query.filter_by(genre_name=request_data['genre_name']).first()
        if genre_check is not None:
            raise GenreDuplicateError(f"Жанр '{genre_check}' уже существует")

        new_genre = Genre(genre_name=request_data['genre_name'])
        db.session.add(new_genre)
        db.session.commit()

    def delete_genre(self, genre_id: int):
        """Находит в БД жанр по ID и удаляет его"""
        genre_to_delete = Genre.query.filter_by(id=genre_id).first()
        if genre_to_delete is None:
            raise GenreNotFoundError("Жанр не найден")

        db.session.delete(genre_to_delete)
        db.session.commit()

    def update_genre(self, genre_id, request_data):
        """Находит в БД жанр по ID и обновляет его название"""
        genre = Genre.query.filter_by(id=genre_id).first()
        if genre is None:
            raise GenreNotFoundError("Жанр не найден")

        genre.genre_name = request_data["genre_name"]
        db.session.commit()

    def delete_all_genres(self):
        genres = Genre.query.all()
        for i in range(len(genres)):
            db.session.delete(genres[i])

        db.session.commit()

    def fill_up_genres_table(self, request_data):
        for row in request_data:
            new_genre = Genre(genre_name=row['genre_name'])
            db.session.add(new_genre)
            db.session.flush()

        db.session.commit()
