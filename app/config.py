import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///fex.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SHOWCASE_TOKEN = os.getenv("SHOWCASE_TOKEN", "dev-showcase-token")
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 1073741824))

    OWNER_USERNAME = os.getenv("OWNER_USERNAME", "admin")
    OWNER_PASSWORD = os.getenv("OWNER_PASSWORD", "admin")