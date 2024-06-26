import json
import random
from collections import Counter

from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash
from application import db, redis_client
from exceptions import (EmailDuplicateError, MangaDuplicateError,
                        MangaNotFoundError, UsernameDuplicateError,
                        UserNotFoundError)
from models import UserManga, Users, Manga, Orders
from utils.email_utils import confirm_registration


class UserService:
    """Класс, описывающий работу с таблицей пользователей в БД"""

    @staticmethod
    def find_user(user_id):
        """Находит пользователя по ID
        в БД и возвращает его в виде словаря"""
        user = Users.query.filter_by(id=user_id).first()
        if user is None:
            raise UserNotFoundError("Пользователь не найден")

        return user.to_dict()

    @staticmethod
    def find_all_users():
        """Возвращает список всех пользователей"""
        all_users = []
        raw_users_list = Users.query.all()
        for row in raw_users_list:
            user = row.to_dict()
            all_users.append(user)

        return all_users

    @staticmethod
    def add_user(request_data):
        """Добавляет нового пользователя в БД"""
        user_check = Users.query.filter_by(username=request_data["username"]).first()
        if user_check:
            raise UsernameDuplicateError("Пользователь с таким именем уже существует")

        user_email_check = Users.query.filter_by(email=request_data["email"]).first()
        if user_email_check:
            raise EmailDuplicateError("Почта занята")

        code = random.randint(100000, 999999)
        confirm_registration(request_data["email"], request_data["username"], code)

        redis_client.set(f"{request_data['username']}-code", code)  # TODO поставить expire?
        redis_client.set(f"{request_data['username']}-data", json.dumps(request_data))
        redis_client.close()

    @staticmethod
    def email_confirmation(request_data):
        if request_data['confirm_code'] == redis_client.get(f"{request_data['username']}-code"):
            new_usermanga = UserManga()
            db.session.add(new_usermanga)
            db.session.flush()

            print(redis_client.get(f"{request_data['username']}-data"))
            user_data = json.loads(redis_client.get(f"{request_data['username']}-data"))

            new_user = Users(username=user_data["username"], psw=generate_password_hash(user_data["psw"]),
                             email=user_data['email'], user_manga_fk=new_usermanga.id, is_admin=False)

            db.session.add(new_user)
            db.session.commit()

            redis_client.delete(f"{request_data['username']}-code")
            redis_client.delete(f"{request_data['username']}-data")
            redis_client.close()

            return {"success": "Почта подтверждена!"}
        else:
            redis_client.close()
            return {"error": "Неверный код!"}

    @staticmethod
    def add_to_cart(user_id, manga_id):
        usermanga = db.session.query(UserManga).join(Users).filter_by(id=user_id).first()

        usermanga_id = usermanga.id
        usermanga_cart = usermanga.cart
        usermanga_fm = usermanga.favorite_manga
        usermanga_pm = usermanga.purchased_manga

        usermanga_cart['cart'].append(manga_id)

        new_usermanga = UserManga(id=usermanga_id, cart=usermanga_cart,
                                  favorite_manga=usermanga_fm, purchased_manga=usermanga_pm)

        db.session.delete(usermanga)
        db.session.add(new_usermanga)
        db.session.commit()

    @staticmethod
    def add_to_favorite(user_id, manga_id):
        usermanga = db.session.query(UserManga).join(Users).filter_by(id=user_id).first()
        if manga_id in usermanga.favorite_manga:
            raise MangaDuplicateError("Эта манга уже в избранном")

        usermanga_id = usermanga.id
        usermanga_cart = usermanga.cart
        usermanga_fm = usermanga.favorite_manga
        usermanga_pm = usermanga.purchased_manga

        usermanga_fm['favorite_manga'].append(manga_id)

        new_usermanga = UserManga(id=usermanga_id, cart=usermanga_cart,
                                  favorite_manga=usermanga_fm, purchased_manga=usermanga_pm)

        db.session.delete(usermanga)
        db.session.add(new_usermanga)
        db.session.commit()

    @staticmethod
    def delete_from_cart(user_id, manga_id):
        usermanga = db.session.query(UserManga).join(Users).filter_by(id=user_id).first()
        if manga_id not in usermanga.cart['cart']:
            raise MangaNotFoundError("В корзине нет этой манги")

        usermanga_id = usermanga.id
        usermanga_cart = usermanga.cart
        usermanga_fm = usermanga.favorite_manga
        usermanga_pm = usermanga.purchased_manga

        usermanga_cart['cart'].remove(manga_id)

        new_usermanga = UserManga(id=usermanga_id, cart=usermanga_cart,
                                  favorite_manga=usermanga_fm, purchased_manga=usermanga_pm)

        db.session.delete(usermanga)
        db.session.add(new_usermanga)
        db.session.commit()

    @staticmethod
    def delete_all_from_cart(user_id, manga_id):
        usermanga = db.session.query(UserManga).join(Users).filter_by(id=user_id).first()
        if manga_id not in usermanga.cart['cart']:
            raise MangaNotFoundError("В корзине нет этой манги")

        usermanga_id = usermanga.id
        usermanga_cart = usermanga.cart
        usermanga_fm = usermanga.favorite_manga
        usermanga_pm = usermanga.purchased_manga

        usermanga_cart['cart'] = list(filter(lambda item: item != manga_id, usermanga_cart['cart']))

        new_usermanga = UserManga(id=usermanga_id, cart=usermanga_cart,
                                  favorite_manga=usermanga_fm, purchased_manga=usermanga_pm)

        db.session.delete(usermanga)
        db.session.add(new_usermanga)
        db.session.commit()

    @staticmethod
    def delete_from_favorite(user_id, manga_id):
        usermanga = db.session.query(UserManga).join(Users).filter_by(id=user_id).first()
        if manga_id not in usermanga.favorite_manga['favorite_manga']:
            raise MangaNotFoundError("В избранном нет этой манги")

        usermanga_id = usermanga.id
        usermanga_cart = usermanga.cart
        usermanga_fm = usermanga.favorite_manga
        usermanga_pm = usermanga.purchased_manga

        usermanga_fm['favorite_manga'].remove(manga_id)

        new_usermanga = UserManga(id=usermanga_id, cart=usermanga_cart,
                                  favorite_manga=usermanga_fm, purchased_manga=usermanga_pm)

        db.session.delete(usermanga)
        db.session.add(new_usermanga)
        db.session.commit()

    @staticmethod
    def auth(request_data):
        user = Users.query.filter_by(username=request_data['username']).first()
        if user and check_password_hash(user.psw, request_data['psw']):
            return {"user_id": user.id}
        else:
            return {"error": "Неверный логин или пароль"}

    @staticmethod
    def get_cart(user_id):
        usermanga = UserManga.query.filter_by(id=user_id).first()
        manga_raw = Manga.query.all()
        cart_ids = usermanga.cart["cart"]

        cart = []
        amount_of_buying = 0
        for row in manga_raw:
            manga = row.to_dict()
            if manga["id"] in cart_ids:
                manga["inCart"] = Counter(cart_ids)[row.id]
                amount_of_buying += row.price * manga["inCart"]
                cart.append(manga)

        return {"cart": cart, "amount_of_buying": amount_of_buying}

    @staticmethod
    def get_favorite_manga(user_id):
        usermanga = UserManga.query.filter_by(id=user_id).first()
        favorite_ids = usermanga.favorite_manga.get('favorite_manga', [])
        manga = Manga.query.all()
        manga = [manga.to_dict() for manga in manga]
        response = []
        for manga in manga:
            if manga["id"] in favorite_ids:
                manga["isFavorite"] = True
                response.append(manga)

        return response

    @staticmethod
    def get_purchased_manga(user_id):
        usermanga = Orders.query.filter_by(client=user_id).all()

        response = []
        for purchase in usermanga:
            response.append({"code": purchase.order_code, "sum": purchase.order_sum, "content": purchase.buying_content["buying_content"]})

        return response

    @staticmethod
    def get_user_manga(user_id):
        manga_list = Manga.query.all()
        user_manga = UserManga.query.get(user_id)

        favorite_ids = user_manga.favorite_manga.get('favorite_manga', [])
        cart_ids = user_manga.cart.get("cart")

        response = []
        for manga in manga_list:
            manga_data = manga.to_dict()
            manga_data["isFavorite"] = manga.id in favorite_ids
            manga_data["inCart"] = Counter(cart_ids)[manga.id]
            response.append(manga_data)

        return response

    @staticmethod
    def get_user_top_manga(user_id):
        manga_list = Manga.query.order_by(func.random()).limit(5).all()
        user_manga = UserManga.query.get(user_id)

        favorite_ids = user_manga.favorite_manga.get('favorite_manga', [])
        cart_ids = user_manga.cart.get("cart")

        response = []
        for manga in manga_list:
            manga_data = manga.to_dict()
            manga_data["isFavorite"] = manga.id in favorite_ids
            manga_data["inCart"] = Counter(cart_ids)[manga.id]
            response.append(manga_data)

        return response
