from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config
from authlib.integrations.flask_client import OAuth
from flask_session import Session
from flasgger import Swagger  # Import Flasgger

# Inicjalizacja globalnych obiektów dla bazy danych, migracji, JWT i OAuth
db = SQLAlchemy()  # Obiekt SQLAlchemy do obsługi bazy danych
migrate = Migrate()  # Obiekt Flask-Migrate do zarządzania migracjami bazy danych
jwt = JWTManager()  # Obiekt JWTManager do obsługi tokenów JWT
oauth = None  # Obiekt OAuth zostanie zainicjalizowany w funkcji create_app
sess = Session()  # Obiekt do obsługi sesji Flask

def create_app():
    # Tworzenie instancji aplikacji Flask
    app = Flask(__name__)
    app.config.from_object(Config)  # Ładowanie konfiguracji z klasy Config
    app.secret_key = app.config["SECRET_KEY"]  # Ustawienie klucza tajnego dla sesji Flask

    # Inicjalizacja obsługi sesji Flask
    sess.init_app(app)  # Konfiguracja sesji na podstawie ustawień w Config

    # Inicjalizacja bazy danych i migracji
    db.init_app(app)  # Powiązanie obiektu SQLAlchemy z aplikacją Flask
    migrate.init_app(app, db)  # Powiązanie obiektu Flask-Migrate z aplikacją i bazą danych

    # Inicjalizacja JWT
    jwt.init_app(app)  # Powiązanie obiektu JWTManager z aplikacją Flask

    # Inicjalizacja OAuth i rejestracja klienta GitHub
    global oauth
    oauth = OAuth(app)  # Tworzenie obiektu OAuth i powiązanie go z aplikacją Flask
    oauth.register(
        name='github',  # Nazwa dostawcy OAuth
        client_id=app.config.get('GITHUB_CLIENT_ID'),  # ID klienta GitHub
        client_secret=app.config.get('GITHUB_CLIENT_SECRET'),  # Sekret klienta GitHub
        access_token_url=app.config.get('GITHUB_ACCESS_TOKEN_URL'),  # URL do uzyskania tokena dostępu
        authorize_url=app.config.get('GITHUB_AUTHORIZE_URL'),  # URL do autoryzacji użytkownika
        api_base_url=app.config.get('GITHUB_API_BASE_URL'),  # Podstawowy URL API GitHub
        client_kwargs={'scope': 'user:email'},  # Zakresy dostępu wymagane przez aplikację
    )

    # Inicjalizacja Flasgger
    Swagger(app)  # Dodanie Flasgger do aplikacji Flask

    # Rejestracja blueprinta dla tras autoryzacyjnych
    from .routes import auth_bp  # Import blueprinta z trasami autoryzacyjnymi
    app.register_blueprint(auth_bp)  # Rejestracja blueprinta w aplikacji Flask

    return app  # Zwrócenie skonfigurowanej aplikacji Flask
