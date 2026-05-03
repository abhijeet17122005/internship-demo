import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Manual SECRET_KEY for session management and flashing
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secret_key_for_internship_demo'
    
    # SQLite Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    
    # Disable modification tracking to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False
