import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from src.config import DevelopmentConfig, ProductionConfig, TestingConfig
from src.persistence.data_manager import DataManager

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

cors = CORS()
db = SQLAlchemy()

def get_config_class():
    """Détermine la configuration à utiliser en fonction des variables d'environnement"""
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        return ProductionConfig
    elif env == 'testing':
        return TestingConfig
    else:
        return DevelopmentConfig

def create_app(config_class=None) -> Flask:
    """
    Create a Flask app with the given configuration class.
    The default configuration class is determined by the FLASK_ENV environment variable.
    """
    if config_class is None:
        config_class = get_config_class()
    
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config_class)
    
    # Initialiser le gestionnaire de données en fonction de la configuration
    data_manager = DataManager(use_database=app.config['USE_DATABASE'])

    register_extensions(app)
    register_routes(app)
    register_handlers(app)

    return app

def register_extensions(app: Flask) -> None:
    """Register the extensions for the Flask app"""
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    # Further extensions can be added here

    # Create tables if they don't exist (only for development purposes)
    with app.app_context():
        if not app.config['USE_DATABASE']:
            db.create_all()

def register_routes(app: Flask) -> None:
    """Import and register the routes for the Flask app"""

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
    app.errorhandler(404)(lambda e: (
        {"error": "Not found", "message": str(e)}, 404
    )
    )
    app.errorhandler(400)(
        lambda e: (
            {"error": "Bad request", "message": str(e)}, 400
        )
    )
