import os
from dotenv import load_dotenv

# Załadowanie zmiennych środowiskowych z pliku .env
load_dotenv()

class Config:
    # Klucz używany do zabezpieczania danych aplikacji (np. sesji). 
    # Jeśli nie zostanie ustawiony w zmiennych środowiskowych, używana jest wartość domyślna.
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key_change_me")
    
    # URI bazy danych, pobierane ze zmiennych środowiskowych.
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    
    # Wyłączenie śledzenia modyfikacji obiektów w SQLAlchemy (optymalizacja wydajności).
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Klucz używany do generowania i weryfikacji tokenów JWT.
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    # Identyfikator klienta GitHub dla autoryzacji OAuth.
    GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
    
    # Sekret klienta GitHub dla autoryzacji OAuth.
    GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
    
    # URL do autoryzacji użytkownika przez GitHub.
    GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
    
    # URL do uzyskania tokena dostępu od GitHub.
    GITHUB_ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token"
    
    # Podstawowy URL API GitHub.
    GITHUB_API_BASE_URL = "https://api.github.com/"
    
    # Typ sesji używany przez aplikację (w tym przypadku plikowy).
    SESSION_TYPE = "filesystem"
    
    # Określa, czy sesje są trwałe (False oznacza, że sesje wygasają po zamknięciu przeglądarki).
    SESSION_PERMANENT = False
    
    # Włączenie podpisywania ciasteczek sesji dla dodatkowego bezpieczeństwa.
    SESSION_USE_SIGNER = True
    
    # Określa, czy ciasteczka sesji są przesyłane tylko przez HTTPS (False dla środowisk deweloperskich).
    SESSION_COOKIE_SECURE = False  # True tylko przy HTTPS

    SWAGGER = {
        "title": "Users API",
        "uiversion": 3,
        "description": "Dokumentacja API dla aplikacji Users",
    }
