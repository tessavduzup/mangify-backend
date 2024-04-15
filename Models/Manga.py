from application import db

# Скачивание манги с сайта???
class Manga(db.Models):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String, nullable=True)
    title = db.Column(db.String, nullable=True)
    wrap = db.Column(db.String, nullable=True)  # Какой тип данных?
    description = db.Column(db.Text, nullable=True)
    genre = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=True)
    amount = db.Column(db.Integer, nullable=True)
    # count = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'author': self.author,
            'title': self.title,
            'wrap': self.wrap,
            'description': self.description,
            'genre_id': self.genre_id,
            'amount': self.amount,
            # 'count': self.count
        }