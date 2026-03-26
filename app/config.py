class Config:
    SECRET_KEY = "secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///inventory.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "jwt-secret"