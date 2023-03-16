import os

# ideally, these should be stored in something like Vault
POSTGRES_URL = os.environ.get("POSTGRES_URL", "localhost")
POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PW = os.environ.get("POSTGRES_PW", "password")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "dev")
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "test_secret_key")


class Config:
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_URL}/{POSTGRES_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_URL}/{POSTGRES_DB}"
    )
