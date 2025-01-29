from flask import Flask


def create_app():
    app = Flask(__name__)

    # Import and register blueprints here (if needed)
    # from .views import views
    # app.register_blueprint(views, url_prefix="/")

    return app
