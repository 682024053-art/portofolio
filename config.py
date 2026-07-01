import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

    TIDB_HOST = os.getenv("TIDB_HOST")
    TIDB_PORT = int(os.getenv("TIDB_PORT", 4000))
    TIDB_USER = os.getenv("TIDB_USER")
    TIDB_PASSWORD = os.getenv("TIDB_PASSWORD")
    TIDB_DATABASE = os.getenv("TIDB_DATABASE")
    CA_PATH = os.getenv("CA_PATH")

    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

    RESEND_API_KEY = os.getenv("RESEND_API_KEY")
    MAIL_FROM = os.getenv("MAIL_FROM")

    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@gmail.com")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
