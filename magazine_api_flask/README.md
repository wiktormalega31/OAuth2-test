# Users API Flask

Projekt API magazynu zbudowany przy użyciu Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-JWT-Extended oraz OAuth z GitHub.

## Wymagania

- Python 3.8 lub nowszy
- PostgreSQL
- Virtualenv (opcjonalnie, ale zalecane)

## Instalacja

1. **Sklonuj repozytorium**:

   ```bash
   git clone <URL_REPOZYTORIUM>
   cd magazine_api_flask
   ```

2. **Utwórz i aktywuj wirtualne środowisko** (opcjonalne, ale zalecane):

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Zainstaluj wymagane pakiety**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Skonfiguruj plik `.env`**:
   Utwórz plik `.env` w katalogu głównym projektu (jeśli jeszcze go nie ma) i skonfiguruj zmienne środowiskowe:

   ```properties
   JWT_SECRET_KEY=super_secret_jwt_key_which_should_be_long_enough
   DATABASE_URL=postgresql://<USER>:<PASSWORD>@<HOST>:<PORT>/<DB_NAME>
   GITHUB_CLIENT_ID=<TWÓJ_CLIENT_ID>
   GITHUB_CLIENT_SECRET=<TWÓJ_CLIENT_SECRET>
   SECRET_KEY=this_is_a_very_long_secret_key_1234567890
   ```

5. **Utwórz bazę danych**:
   Upewnij się, że baza danych PostgreSQL jest uruchomiona i skonfigurowana zgodnie z `DATABASE_URL` w pliku `.env`.

6. **Zainicjalizuj bazę danych**:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

## Uruchomienie

1. **Uruchom aplikację**:

   ```bash
   python run.py
   ```

2. **Otwórz aplikację w przeglądarce**:
   Domyślnie aplikacja działa pod adresem: [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Testowanie

- **Rejestracja użytkownika**:
  Endpoint: `POST /register`  
  Payload:

  ```json
  {
    "email": "example@example.com",
    "name": "Example User",
    "password": "examplepassword"
  }
  ```

- **Logowanie użytkownika**:
  Endpoint: `POST /login`  
  Payload:

  ```json
  {
    "email": "example@example.com",
    "password": "examplepassword"
  }
  ```

- **Logowanie przez GitHub**:
  Endpoint: `GET /oauth2/redirect`  
  Opis: Przekierowuje użytkownika do strony logowania GitHub. Po zalogowaniu użytkownik zostanie przekierowany na endpoint callbacka.

- **Callback OAuth**:
  Endpoint: `GET /oauth2/callback`  
  Opis: Obsługuje odpowiedź z GitHub po autoryzacji. Zwraca token JWT, który można użyć do autoryzacji w aplikacji.  
  Przykładowa odpowiedź:

  ```json
  {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```

- **Testowanie chronionego endpointu**:
  Endpoint: `GET /protected`  
  Nagłówki:
  ```http
  Authorization: Bearer <TOKEN>
  ```
  Opis: Zwraca listę użytkowników w bazie danych. Wymaga poprawnego tokena JWT.

## Dodatkowe informacje

- **Migracje bazy danych**:

  - Tworzenie nowej migracji:
    ```bash
    flask db migrate -m "Opis migracji"
    ```
  - Aktualizacja bazy danych:
    ```bash
    flask db upgrade
    ```

- **Debugowanie**:
  Aby włączyć tryb debugowania, ustaw `debug=True` w pliku `run.py`.
