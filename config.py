import os

class Config:
    # Postgres Cloud SQL connection via Unix socket
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@/"
        f"{os.environ['DB_NAME']}?host=/cloudsql/{os.environ['DB_HOST']}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SECRET_KEY required for flash messages and sessions
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')  # fallback if env var missing
