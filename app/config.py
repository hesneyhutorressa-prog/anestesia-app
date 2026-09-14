import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "clave-secreta-desarrollo-cambiar-en-produccion")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "anestesia.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER_MANUALES = os.path.join(BASE_DIR, "app", "static", "uploads", "manuales")
    UPLOAD_FOLDER_EVIDENCIAS = os.path.join(BASE_DIR, "app", "static", "uploads", "evidencias")
    QR_FOLDER = os.path.join(BASE_DIR, "app", "static", "qrcodes")

    MAX_CONTENT_LENGTH = 10 * 1024 * 1024