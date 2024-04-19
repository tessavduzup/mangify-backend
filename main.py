from application import app, api
from Controllers.genre_controller import GenreController
from Controllers.user_controller import UserController
from Controllers.manga_controller import MangaController

if __name__ == '__main__':
    api.add_resource(GenreController)
    api.add_resource(UserController)
    api.add_resource(MangaController)
    app.run(debug=True)