"""
Configuración por entornos – Green House Inmobiliaria
"""
import os
from dotenv import load_dotenv

load_dotenv()

class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'greenhouse-secret-key-dev-2025')
    JSON_SORT_KEYS = False
    JSON_AS_ASCII = False  # Soportar caracteres españoles

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    # Email simulado en desarrollo (no envía realmente)
    MAIL_ENABLED = False
    MAIL_FROM = 'info@greenhouseleganes.es'

class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    MAIL_ENABLED = True
    MAIL_FROM = os.getenv('MAIL_FROM', 'info@greenhouseleganes.es')
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    MAIL_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
