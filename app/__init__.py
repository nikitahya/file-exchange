from flask import Flask

from app.config import Config
from app.extensions import db, login_manager
from app.showcase import showcase_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from app import models  # noqa: F401
        db.create_all()

    from app.auth import auth_bp
    from app.views import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(showcase_bp)

    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app