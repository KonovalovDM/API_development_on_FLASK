from app.database import db

class User(db.Model):
    """
    Модель пользователя.
    Атрибуты:
        id (int): Уникальный идентификатор пользователя.
        username (str): Имя пользователя, уникальное и обязательное.
        posts (list[Post]): Связанные публикации.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)


class Post(db.Model):
    """
    Модель публикации.
    Атрибуты:
        id (int): Уникальный идентификатор публикации.
        title (str): Заголовок публикации.
        content (str): Содержимое публикации.
        user_id (int): Идентификатор пользователя, связанного с публикацией.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
