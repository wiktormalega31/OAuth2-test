from flask import Blueprint, request, jsonify, url_for, redirect
from .models import User
from . import db, oauth
from .auth import generate_token
from flask_jwt_extended import jwt_required

# Utworzenie blueprinta dla tras autoryzacyjnych
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Rejestracja nowego użytkownika
    ---
    tags:
      - JWT
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
            name:
              type: string
            password:
              type: string
    responses:
      201:
        description: Użytkownik został utworzony
      400:
        description: Błąd walidacji lub użytkownik już istnieje
    """
    # Rejestracja nowego użytkownika
    data = request.get_json()  # Pobranie danych z żądania
    if "password" not in data:
        return jsonify({"message": "Brakuje pola 'password'"}), 400  # Walidacja danych wejściowych

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "User already exists"}), 400  # Sprawdzenie, czy użytkownik już istnieje

    # Tworzenie nowego użytkownika
    user = User(email=data["email"], name=data["name"])
    user.set_password(data["password"])  # Ustawienie hasła
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Logowanie użytkownika
    ---
    tags:
      - JWT
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: Zwraca token JWT
      401:
        description: Niepoprawne dane logowania
    """
    # Logowanie użytkownika
    data = request.get_json()  # Pobranie danych z żądania
    user = User.query.filter_by(email=data["email"]).first()  # Wyszukanie użytkownika po emailu
    if user and user.check_password(data["password"]):  # Sprawdzenie poprawności hasła
        token = generate_token(user)  # Generowanie tokena JWT
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 401  # Niepoprawne dane logowania

@auth_bp.route("/oauth2/redirect", methods=["GET"])
def github_login():
    """
    Przekierowanie użytkownika do GitHub OAuth2
    ---
    tags:
      - OAuth
    responses:
      302:
        description: Przekierowanie do GitHub w celu autoryzacji
    """
    # Przekierowanie użytkownika do GitHub OAuth2
    redirect_uri = url_for("auth.github_callback", _external=True)  # URL callbacka
    return oauth.github.authorize_redirect(redirect_uri)  # Przekierowanie do GitHub

@auth_bp.route("/oauth2/callback", methods=["GET"])
def github_callback():
    """
    Obsługa callbacka po autoryzacji GitHub
    ---
    tags:
      - OAuth
    responses:
      200:
        description: Zwraca token JWT po pomyślnej autoryzacji
      400:
        description: Błąd podczas autoryzacji OAuth
    """
    # Obsługa callbacka po autoryzacji GitHub
    try:
        token = oauth.github.authorize_access_token()  # Uzyskanie tokena dostępu
        resp = oauth.github.get("user", token=token)  # Pobranie danych użytkownika z GitHub
        profile = resp.json()
    except Exception as e:
        return jsonify({"message": f"OAuth error: {str(e)}"}), 400  # Obsługa błędów OAuth

    # Pobranie emaila użytkownika
    email = profile.get("email")
    if not email:
        resp_emails = oauth.github.get("user/emails", token=token)  # Pobranie emaili, jeśli nie są publiczne
        emails = resp_emails.json()
        email = next((e["email"] for e in emails if e.get("primary") and e.get("verified")), None)

    if not email:
        return jsonify({"message": "Unable to retrieve email from GitHub"}), 400  # Brak emaila

    # Wyszukanie lub utworzenie użytkownika
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, name=profile.get("login", "GitHub User"))
        user.set_password(None)  # Ustawienie pustego hasła dla konta OAuth
        db.session.add(user)
        db.session.commit()

    jwt_token = generate_token(user)  # Generowanie tokena JWT
    return jsonify({"token": jwt_token}), 200  # Zwrócenie tokena JWT

@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    """
    Przykładowy chroniony endpoint
    ---
    tags:
      - Protected
    responses:
      200:
        description: Zwraca listę użytkowników
    """
    # Przykładowy chroniony endpoint
    users = User.query.all()  # Pobranie wszystkich użytkowników
    users_data = [{"id": user.id, "email": user.email, "name": user.name} for user in users]
    return jsonify(users_data), 200  # Zwrócenie danych użytkowników
