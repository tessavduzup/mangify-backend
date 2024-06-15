from application import api, app
from controllers import GenreController, MangaController, UserController, UnnecessaryController
from payment import WalletController

if __name__ == '__main__':
    api.add_resource(GenreController)
    api.add_resource(UserController)
    api.add_resource(MangaController)
    api.add_resource(WalletController)
    api.add_resource(UnnecessaryController)

    app.run(debug=True)
