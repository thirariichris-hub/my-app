import os

class Config:
    SECRET_KEY = "secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(os.path.dirname(__file__), "../instance/inventory.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

