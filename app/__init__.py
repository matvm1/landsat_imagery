from flask import Flask
from ee import Authenticate as ee_Auth, Initialize as ee_Init


def create_app():
    app = Flask(__name__)

    # Import and register blueprints here (if needed)
    # from .views import views
    # app.register_blueprint(views, url_prefix="/")

    return app


def init_lsatimg_service():
    """Authenticate and initialize Google Earth Engine."""
    try:
        ee_Auth()
        ee_Init(project='ee-city-center-detector')
        print('Google Earth Engine initialized successfully')
    except Exception as e:
        print(f"Error initializing GEE: {e}")