from flask import jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from application import db
from exceptions import (MangaDuplicateError, MangaNotFoundError,
                        UsernameDuplicateError, UserNotFoundError)
from Models import UserManga, Users


class UserService:
    """Класс, описывающий работу с таблицей пользователей в БД"""

    def auth(self, request_data):  # TODO
        user = Users.query.filter_by(username=request_data['username']).first()
        if user and check_password_hash(user.psw, request_data['psw']):
            return jsonify({"id": user.id})
        else:
            return jsonify({"error": "Неверный логин или пароль"})

    def find_user(self, user_id):
        """Находит пользователя по ID
        в БД и возвращает его в виде словаря"""
        user = Users.query.filter_by(id=user_id).first()
        if user is None:
            raise UserNotFoundError("Пользователь не найден")

        return user.to_dict()

    def find_all_users(self):
        """Возвращает список всех пользователей"""
        all_users = []
        raw_users_list = Users.query.all()
        for row in raw_users_list:
            user = row.to_dict()
            all_users.append(user)

        return all_users

    def add_user(self, request_data):
        """Добавляет нового пользователя в БД"""
        user_check = Users.query.filter_by(username=request_data["username"]).first()
        if user_check:
            raise UsernameDuplicateError("Пользователь с таким именем уже существует")

        new_usermanga = UserManga()
        db.session.add(new_usermanga)
        db.session.flush()

        new_user = Users(username=request_data["username"], psw=generate_password_hash(request_data["psw"]),
                         user_manga_fk=new_usermanga.id, is_admin=False)  # Система ролей?

        db.session.add(new_user)
        db.session.commit()

    def delete_user(self, user_id: int):
        """Находит в БД пользователя по ID и удаляет его"""
        user_to_delete = Users.query.filter_by(id=user_id).first()
        if not user_to_delete:
            raise UserNotFoundError("Пользователь не найден")

        db.session.delete(user_to_delete)
        db.session.commit()

    def update_user(self, user_id, request_data):
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

    def add_to_cart(self, user_id, manga_id):
        usermanga = db.session.query(UserManga).join(Users).filter_by(id=user_id).first()
        if manga_id in usermanga.cart:
            raise MangaDuplicateError("Эта манга уже в корзине")

        usermanga_id = usermanga.id
        usermanga_cart = usermanga.cart
        usermanga_fm = usermanga.favourite_manga
        usermanga_pm = usermanga.purchased_manga

        usermanga_cart['cart'].append(manga_id)

        new_usermanga = UserManga(id=usermanga_id, cart=usermanga_cart,
                                  favourite_manga=usermanga_fm, purchased_manga=usermanga_pm)

        db.session.delete(usermanga)
        db.session.add(new_usermanga)
        db.session.commit()

    def add_to_favourite(self, user_id, manga_id):
        usermanga = db.session.query(UserManga).join(Users).filter_by(id=user_id).first()
        if manga_id in usermanga.favourite_manga:
            raise MangaDuplicateError("Эта манга уже в избранном")

        usermanga_id = usermanga.id
        usermanga_cart = usermanga.cart
        usermanga_fm = usermanga.favourite_manga
        usermanga_pm = usermanga.purchased_manga

        usermanga_fm['favourite_manga'].append(manga_id)

        new_usermanga = UserManga(id=usermanga_id, cart=usermanga_cart,
                                  favourite_manga=usermanga_fm, purchased_manga=usermanga_pm)

        db.session.delete(usermanga)
        db.session.add(new_usermanga)
        db.session.commit()

    def delete_from_cart(self, user_id, manga_id):
        usermanga = db.session.query(UserManga).join(Users).filter_by(id=user_id).first()
        if manga_id not in usermanga.cart:
            raise MangaNotFoundError("В корзине нет этой манги")

        usermanga_id = usermanga.id
        usermanga_cart = usermanga.cart
        usermanga_fm = usermanga.favourite_manga
        usermanga_pm = usermanga.purchased_manga

        usermanga_cart['cart'].remove(manga_id)

        new_usermanga = UserManga(id=usermanga_id, cart=usermanga_cart,
                                  favourite_manga=usermanga_fm, purchased_manga=usermanga_pm)

        db.session.delete(usermanga)
        db.session.add(new_usermanga)
        db.session.commit()

    def delete_from_favourite(self, user_id, manga_id):
        usermanga = db.session.query(UserManga).join(Users).filter_by(id=user_id).first()
        if manga_id not in usermanga.favourite_manga:
            raise MangaNotFoundError("В избранном нет этой манги")

        usermanga_id = usermanga.id
        usermanga_cart = usermanga.cart
        usermanga_fm = usermanga.favourite_manga
        usermanga_pm = usermanga.purchased_manga

        usermanga_fm['favourite_manga'].remove(manga_id)

        new_usermanga = UserManga(id=usermanga_id, cart=usermanga_cart,
                                  favourite_manga=usermanga_fm, purchased_manga=usermanga_pm)

        db.session.delete(usermanga)
        db.session.add(new_usermanga)
        db.session.commit()

    def delete_all_users(self):
        users = Users.query.all()
        for i in range(len(users)):
            db.session.delete(users[i])

        db.session.commit()

    def fill_up_users_table(self, request_data):
        for row in request_data:
            new_user = Users(username=row["username"], email=row["email"],
                             psw=generate_password_hash(row["psw"]))

            db.session.add(new_user)
            db.session.flush()

        db.session.commit()
