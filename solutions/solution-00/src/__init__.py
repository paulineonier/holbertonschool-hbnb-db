""" Initialize the Flask app """

from flask import Flask
from .extensions import cors, db
from src.persistence.data_manager import DataManager
from flask import Flask
from .config import DevelopmentConfig
from .routes import register_routes

def create_app(config_class="src.config.DevelopmentConfig") -> Flask:
    """
    Create a Flask app with the given configuration class.
    The default configuration class is DevelopmentConfig.
    """
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config_class)

    # Initialize extensions
    initialize_extensions(app)

    data_manager = DataManager(use_database=app.config['USE_DATABASE'])

    register_routes(app)
    register_handlers(app)

    return app

def initialize_extensions(app: Flask) -> None:
    """Initialize Flask extensions"""
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    # Other extensions initialization can be added here

    # Create tables if they don't exist (only for development purposes)
    with app.app_context():
        db.create_all()

def register_routes(app: Flask) -> None:
    """Register the routes for the Flask app"""

    # Import the routes here to avoid circular imports
    from src.routes.users import users_bp
    from src.routes.countries import countries_bp
    from src.routes.cities import cities_bp
    from src.routes.places import places_bp
    from src.routes.amenities import amenities_bp
    from src.routes.reviews import reviews_bp

    # Register the blueprints in the app
    app.register_blueprint(users_bp)
    app.register_blueprint(countries_bp)
    app.register_blueprint(cities_bp)
    app.register_blueprint(places_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(amenities_bp)

def register_handlers(app: Flask) -> None:
    """Register the error handlers for the Flask app."""
    @app.errorhandler(404)
    def handle_not_found_error(e):
        return {"error": "Not found", "message": str(e)}, 404

    @app.errorhandler(400)
    def handle_bad_request_error(e):
        return {"error": "Bad request", "message": str(e)}, 400
