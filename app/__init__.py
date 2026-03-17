
from flask import Flask

from app.config import Config
from app.extensions import db, login_manager
from app.utils import format_datetime, generate_showcase_token

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    app.jinja_env.filters["datetime"] = format_datetime

    with app.app_context():
        from app import models  # noqa: F401
        from app.models import ShowcaseState

        db.create_all()

        state = ShowcaseState.query.first()
        if not state:
            state = ShowcaseState(
                id=1,
                mode="empty",
                active_post_id=None,
                token=generate_showcase_token(),
            )
            db.session.add(state)
            db.session.commit()

    from app.auth import auth_bp
    from app.views import main_bp
    from app.showcase import showcase_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(showcase_bp)

    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app