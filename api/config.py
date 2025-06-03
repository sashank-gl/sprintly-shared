import os

class Config:
    # Without Password
    # SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://localhost/database_name")

    # With Password
    # SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost/database_name")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

class DevConfig(Config):
    pass

class ProdConfig(Config):
    DEBUG = False