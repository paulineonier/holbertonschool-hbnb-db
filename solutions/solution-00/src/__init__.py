from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from .extensions import cors, db
from .config import DevelopmentConfig
from src.persistence.data_manager import DataManager
from .routes import register_routes

bcrypt = Bcrypt()
jwt = JWTManager()

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
    bcrypt.init_app(app)
    jwt.init_app(app)
    # Other extensions initialization can be added here

    from src.models.city import City
    from src.models.country import Country
    from src.models.place import Place
    from src.models.review import Review
    from src.models.amenity import Amenity
    from src.models.user import User

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
    from src.routes.reviews import reviews_bp
    from src.routes.amenities import amenities_bp

    # Register the blueprints in the app
    app.register_blueprint(users_bp)
    app.register_blueprint(countries_bp)
    app.register_blueprint(cities_bp)
    app.register_blueprint(places_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(amenities_bp)

    # Register the login route
    @app.route('/login', methods=['POST'])
    def login():
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token), 200
        return jsonify({"msg": "Email ou mot de passe incorrect"}), 401

    # Example of a protected route
    @app.route('/protected', methods=['GET'])
    @jwt_required()
    def protected():
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        return jsonify(logged_in_as=user.email), 200

def register_handlers(app: Flask) -> None:
    """Register the error handlers for the Flask app."""
    @app.errorhandler(404)
    def handle_not_found_error(e):
        return {"error": "Not found", "message": str(e)}, 404

    @app.errorhandler(400)
    def handle_bad_request_error(e):
        return {"error": "Bad request", "message": str(e)}, 400
