from flask import Flask
from .config import Config
from .extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from .views.user_views import user_bp
    from .views.product_views import product_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(product_bp)

    @app.errorhandler(404)
    def not_found(error):
        from flask import jsonify
        from datetime import datetime
        return jsonify({'error': 'Not found', 'timestamp': datetime.utcnow().isoformat()}), 404

    @app.errorhandler(500)
    def internal_error(error):
        from flask import jsonify
        from datetime import datetime
        db.session.rollback()
        return jsonify({'error': 'Internal server error', 'timestamp': datetime.utcnow().isoformat()}), 500

    @app.errorhandler(400)
    def bad_request(error):
        from flask import jsonify
        from datetime import datetime
        return jsonify({'error': 'Bad Request', 'message': str(error.description or error), 'timestamp': datetime.utcnow().isoformat()}), 400

    return app

