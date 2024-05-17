from application import app, api
from controllers import GenreController, UserController, MangaController
from payment import WalletController

if __name__ == '__main__':
    api.add_resource(GenreController)
    api.add_resource(UserController)
    api.add_resource(MangaController)
    api.add_resource(WalletController)

    app.run(debug=True)
