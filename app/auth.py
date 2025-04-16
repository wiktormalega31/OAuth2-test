from flask_jwt_extended import create_access_token

def generate_token(user):
    # Generowanie tokena JWT dla użytkownika
    # identity - unikalny identyfikator użytkownika (np. ID)
    # additional_claims - dodatkowe dane (np. email) dodane do tokena
    return create_access_token(identity=str(user.id), additional_claims={"email": user.email})
