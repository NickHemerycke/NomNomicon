import os

class Config:
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@/"
        f"{os.environ['DB_NAME']}?host=/cloudsql/{os.environ['DB_HOST']}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
