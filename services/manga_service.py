from sqlalchemy import func
from exceptions import MangaNotFoundError
from models import Manga


class MangaService:
    """Класс, описывающий работу с таблицей для манги в БД"""

    @staticmethod
    def find_manga(manga_id):
        """Находит мангу по ID
        в БД и возвращает его в виде словаря"""
        manga = Manga.query.filter_by(id=manga_id).first()
        if manga is None:
            raise MangaNotFoundError("Манга не найдена")

        return manga.to_dict()

    @staticmethod
    def find_all_manga():
        """Возвращает список всей
        манги, находящейся в БД"""
        all_manga = []
        raw_manga_list = Manga.query.all()
        for row in raw_manga_list:
            manga = row.to_dict()
            all_manga.append(manga)

        return all_manga

    @staticmethod
    def find_similar_manga(manga_id):
        main_manga = Manga.query.filter_by(id=manga_id).first()
        if not main_manga:
            raise MangaNotFoundError

        manga_genres = main_manga.genre
        similar_manga = Manga.query.filter_by(genre=manga_genres).all()

        return similar_manga

    @staticmethod
    def find_top_manga():
        """Возвращает список популярной манги"""
        top_manga = []
        raw_manga_list = Manga.query.order_by(func.random()).limit(5).all()
        for row in raw_manga_list:
            manga = row.to_dict()
            top_manga.append(manga)

        return top_manga
