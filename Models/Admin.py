from User import User


class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)

    def is_admin(self):
        return True
