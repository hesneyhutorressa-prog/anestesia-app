from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = app.config["SECRET_KEY"]

    db.init_app(app)

    from .routes.main import main_bp
    from .routes.equipos import equipos_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(equipos_bp)

    with app.app_context():
        db.create_all()

    return app