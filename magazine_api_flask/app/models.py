from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'  # Nazwa tabeli w bazie danych

    # Definicja kolumn w tabeli
    id = db.Column(db.Integer, primary_key=True)  # Klucz główny
    email = db.Column(db.String(120), unique=True, nullable=False)  # Unikalny email użytkownika
    name = db.Column(db.String(120), nullable=False)  # Imię/nazwa użytkownika
    password_hash = db.Column(db.Text, nullable=True)  # Hash hasła (może być null dla OAuth)

    def set_password(self, password):
        # Ustawienie hasła użytkownika (hashowanie hasła)
        self.password_hash = generate_password_hash(password) if password else None

    def check_password(self, password):
        # Sprawdzenie poprawności hasła
        if not self.password_hash:  # Jeśli brak hasła (np. konto OAuth), zwróć False
            return False
        return check_password_hash(self.password_hash, password)  # Porównanie hasła z hashem
