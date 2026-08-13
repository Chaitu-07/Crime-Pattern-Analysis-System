import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    SECRET_KEY = os.getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.getenv("postgresql://crime_pattern_db_user:INZYhXBHQ5fqXqsnMQUsqRAmfxR2AxAP@dpg-d9v0f9ajobas73bvnl5g-a/crime_pattern_db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = "uploads"

    MAX_CONTENT_LENGTH = 20 * 1024 * 1024

    ALLOWED_EXTENSIONS = {"csv"}
