from sqlalchemy import func
from application import db
from Models.Genre import Genre
from Models.Image import Image
from Models.Manga import Manga


class MangaService:
    """Класс, описывающий работу с таблицей для манги в БД"""

    def find_manga(self, manga_id):
        """Находит мангу по ID
        в БД и возвращает его в виде словаря"""
        manga = Manga.query.filter_by(id=manga_id).first()
        return manga.to_dict()

    def find_all_manga(self):
        """Возвращает список всей
        манги, находящейся в БД"""
        all_manga = []
        raw_manga_list = Manga.query.all()
        for row in raw_manga_list:
            manga = row.to_dict()
            all_manga.append(manga)

        return all_manga

    def find_top_manga(self):
        """Возвращает список популярной манги"""
        top_manga = []
        raw_manga_list = Manga.query.order_by(func.random()).limit(5).all()
        for row in raw_manga_list:
            manga = row.to_dict()
            top_manga.append(manga)

        return top_manga

    def add_manga(self, request_data):
        """По данным запроса добавляет новую мангу в БД"""
        new_wrap = Image(wrap_path=request_data['wrap_path'])

        db.session.add(new_wrap)
        db.session.flush()

        genres = request_data['genre']
        genres_id = []
        for genre in genres:
            genre_row = Genre.query.filter_by(genre_name=genre).first()
            if genre_row:
                genres_id.append(genre_row.genre_name)
            else:
                new_genre = Genre(genre_name=genre)
                db.session.add(new_genre)
                db.session.commit()
                genres_id.append(new_genre.genre_name)

        new_manga = Manga(author=request_data['author'], title=request_data['title'],
                          title_en=request_data['title-en'], wrap_fk=new_wrap.id,
                          description=request_data['description'], genre={"genres": genres_id},
                          price=request_data['price'])

        db.session.add(new_manga)
        db.session.commit()

    def delete_manga(self, manga_id: int):
        """Находит в БД мангу по ID и удаляет её"""
        manga_to_delete = Manga.query.filter_by(id=manga_id).first()
        db.session.delete(manga_to_delete)
        db.session.commit()

    def update_manga(self, manga_id, request_data):
        """Находит в БД мангу по ID и обновляет её данные"""
        manga = Manga.query.filter_by(id=manga_id).first()
        for key in request_data:
            setattr(manga, key, request_data[key])

        db.session.commit()

    def delete_all_manga(self):
        manga = Manga.query.all()
        for i in range(len(manga)):
            db.session.delete(manga[i])

        db.session.flush()

        images = Image.query.all()
        for i in range(len(images)):
            db.session.delete(images[i])

        db.session.commit()

    def fill_up_manga_table(self, request_data):
        for row in request_data:
            new_wrap = Image(wrap_path=row['wrap_path'])

            db.session.add(new_wrap)
            db.session.flush()

            genres = row['genre']
            genres_id = []
            for genre in genres:
                genre_row = Genre.query.filter_by(genre_name=genre).first()
                if genre_row:
                    genres_id.append(genre_row.id)
                else:
                    new_genre = Genre(genre_name=genre)
                    db.session.add(new_genre)
                    db.session.commit()
                    genres_id.append(new_genre.id)

            new_manga = Manga(author=row['author'], title=row['title'],
                              title_en=row['title-en'], wrap_fk=new_wrap.id,
                              description=row['description'], genre=genres_id,
                              price=row['price'])

            db.session.add(new_manga)
            db.session.commit()
