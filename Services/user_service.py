from Models.Users import Users
from application import db
from werkzeug.security import generate_password_hash


class UserService:
    """Класс, описывающий работу с таблицей пользователей в БД"""

    def find_user(self, user_id):
        """Находит пользователя по ID
        в БД и возвращает его в виде словаря"""
        user = Users.query.filter_by(id=user_id).first()
        return user.to_dict()

    def find_all_users(self):
        """Возвращает список всех пользователей"""
        all_users = []
        raw_users_list = Users.query.all()
        for row in raw_users_list:
            user = row.to_dict()
            all_users.append(user)

        return raw_users_list

    def add_user(self, request_data):
        """Добавляет нового пользователя в БД"""
        new_user = Users(username=request_data["username"], email=request_data["email"],
                        psw=generate_password_hash(request_data["psw"]))
        db.session.add(new_user)
        db.session.commit()

    def delete_user(self, user_id: int):
        """Находит в БД пользователя по ID и удаляет его"""
        user_to_delete = Users.query.filter_by(id=user_id).first()
        db.session.delete(user_to_delete)
        db.session.commit()

    def update_user(self, user_id, request_data):
        """Находит в БД пользователя по ID и обновляет его данные"""
        user = Users.query.filter_by(id=user_id).first()
        for key in request_data:
            setattr(user, key, request_data[key])

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