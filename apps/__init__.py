import settings
from flask import Flask
from exts import db

from apps.user.view import user_bp


def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(settings.DevelopmentConfig)
    db.init_app(app)
    app.register_blueprint(user_bp)
    print(app.url_map)
    return app
