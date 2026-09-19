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
    from .routes.hoja_vida import hoja_vida_bp
    from .routes.inventario import inventario_bp
    from .routes.checklist import checklist_bp
    from .routes.historial import historial_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(equipos_bp)
    app.register_blueprint(hoja_vida_bp)
    app.register_blueprint(inventario_bp)
    app.register_blueprint(checklist_bp)
    app.register_blueprint(historial_bp)

    with app.app_context():
        db.create_all()

    return app