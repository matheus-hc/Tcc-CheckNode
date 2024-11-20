import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()  

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)  
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///banco_dados.db'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=15)

    
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME') 
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD') 
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
