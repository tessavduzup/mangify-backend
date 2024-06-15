from werkzeug.security import generate_password_hash
from application import db
from exceptions import (MangaDuplicateError,
                        MangaNotFoundError, UsernameDuplicateError,
                        UserNotFoundError, GenreNotFoundError)
from models import Users, Genre, Image, Manga


class UnnecessaryService:
    @staticmethod
    def delete_user(user_id: int):
        """Находит в БД пользователя по ID и удаляет его"""
        user_to_delete = Users.query.filter_by(id=user_id).first()
        if not user_to_delete:
            raise UserNotFoundError("Пользователь не найден")

        db.session.delete(user_to_delete)
        db.session.commit()

    @staticmethod
    def update_user(user_id, request_data):
        """Находит в БД пользователя по ID и обновляет его данные"""
        user = Users.query.filter_by(id=user_id).first()
        if not user:
            raise UserNotFoundError("Пользователь не найден")

        user_check = Users.query.filter_by(username=request_data["username"]).first()
        if user_check:
            raise UsernameDuplicateError("Пользователь с таким именем уже существует")

        for key in request_data:
            setattr(user, key, request_data[key])

        db.session.commit()

    @staticmethod
    def delete_all_users():
        users = Users.query.all()
        for i in range(len(users)):
            db.session.delete(users[i])

        db.session.commit()

    @staticmethod
    def fill_up_users_table(request_data):
        for row in request_data:
            new_user = Users(username=row["username"], email=row["email"],
                             psw=generate_password_hash(row["psw"]))

            db.session.add(new_user)
            db.session.flush()

        db.session.commit()

    @staticmethod
    def delete_all_manga():
        manga = Manga.query.all()
        for i in range(len(manga)):
            db.session.delete(manga[i])

        db.session.flush()

        images = Image.query.all()
        for i in range(len(images)):
            db.session.delete(images[i])

        db.session.commit()

    @staticmethod
    def fill_up_manga_table(request_data):
        for row in request_data:
            new_wrap = Image(wrap_path=row['wrap_path'])

            db.session.add(new_wrap)
            db.session.flush()

            genres = row['genre']
            genres_name = []
            for genre in genres:
                genre_row = Genre.query.filter_by(genre_name=genre).first()
                if genre_row:
                    genres_name.append(genre_row.genre_name)
                else:
                    new_genre = Genre(genre_name=genre)
                    db.session.add(new_genre)
                    db.session.commit()
                    genres_name.append(new_genre.id)

            new_manga = Manga(author=row['author'], title=row['title'],
                              title_en=row['title-en'], wrap_fk=new_wrap.id,
                              description=row['description'], genre=genres_name,
                              price=row['price'])

            db.session.add(new_manga)
            db.session.commit()

    @staticmethod
    def add_manga(request_data):
        """По данным запроса добавляет новую мангу в БД"""
        new_wrap = Image(wrap_path=request_data['wrap_path'])

        db.session.add(new_wrap)
        db.session.flush()

        genres = request_data['genre']
        genres_name = []
        for genre in genres:
            genre_row = Genre.query.filter_by(genre_name=genre).first()
            if genre_row:
                genres_name.append(genre_row.genre_name)
            else:
                raise GenreNotFoundError("Жанр не найден")

        title_check = Manga.query.filter_by(title=request_data['title']).first()
        if title_check:
            raise MangaDuplicateError(f"Манга '{request_data['title']}' уже существует")

        new_manga = Manga(author=request_data['author'], title=request_data['title'],
                          title_en=request_data['title-en'], wrap_fk=new_wrap.id,
                          description=request_data['description'], genre={"genres": genres_name},
                          price=request_data['price'])

        db.session.add(new_manga)
        db.session.commit()

    @staticmethod
    def delete_manga(manga_id: int):
        """Находит в БД мангу по ID и удаляет её"""
        manga_to_delete = Manga.query.filter_by(id=manga_id).first()
        if manga_to_delete is None:
            raise MangaNotFoundError("Манга не найдена")

        db.session.delete(manga_to_delete)
        db.session.commit()

    @staticmethod
    def update_manga(manga_id, request_data):
        """Находит в БД мангу по ID и обновляет её данные"""
        manga = Manga.query.filter_by(id=manga_id).first()
        if manga is None:
            raise MangaNotFoundError("Манга не найдена")

        for key in request_data:
            setattr(manga, key, request_data[key])

        db.session.commit()
