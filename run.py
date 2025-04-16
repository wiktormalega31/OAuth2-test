from app import create_app  # Import funkcji tworzącej aplikację Flask

# Tworzenie instancji aplikacji Flask
app = create_app()

if __name__ == "__main__":
    # Uruchomienie aplikacji w trybie debugowania
    # Debug=True pozwala na automatyczne przeładowanie aplikacji przy zmianach w kodzie
    app.run(debug=True)
