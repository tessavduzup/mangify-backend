from application import app, api
from Controllers.genre_controller import GenreController
from Controllers.user_controller import UserController
from Controllers.manga_controller import MangaController
from Payment.Controllers.wallet_controller import WalletController

if __name__ == '__main__':
    api.add_resource(GenreController)
    api.add_resource(UserController)
    api.add_resource(MangaController)
    api.add_resource(WalletController)

    app.run(debug=True)