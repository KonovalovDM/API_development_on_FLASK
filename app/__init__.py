from flask import Flask
from app.database import db

def create_app():
    """Инициализирует Flask-приложение и подключает базу данных."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Регистрация маршрутов
    with app.app_context():
        from app.routes import main_bp
        app.register_blueprint(main_bp)
        db.create_all()

    return app
