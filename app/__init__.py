from flask import Flask
from .config import Config
from .extensions import db, jwt

from routes.user_routes import user_bp
from routes.product_routes import product_bp
from routes.category_routes import category_bp
from routes.supplier_routes import supplier_bp
from routes.transaction_routes import transaction_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(product_bp, url_prefix="/api/products")
    app.register_blueprint(category_bp, url_prefix="/api/categories")
    app.register_blueprint(supplier_bp, url_prefix="/api/suppliers")
    app.register_blueprint(transaction_bp, url_prefix="/api/transactions")

    return app