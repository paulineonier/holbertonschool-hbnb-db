from flask import Blueprint

# Création des Blueprints pour chaque module
users_bp = Blueprint('users', __name__, url_prefix='/api/users')
countries_bp = Blueprint('countries', __name__, url_prefix='/api/countries')
cities_bp = Blueprint('cities', __name__, url_prefix='/api/cities')
places_bp = Blueprint('places', __name__, url_prefix='/api/places')
amenities_bp = Blueprint('amenities', __name__, url_prefix='/api/amenities')
reviews_bp = Blueprint('reviews', __name__, url_prefix='/api/reviews')

# Import des vues/routeurs pour chaque Blueprint
from . import users, countries, cities, places, amenities, reviews

# Enregistrement des Blueprints dans l'application Flask
def register_routes(app):
    app.register_blueprint(users_bp)
    app.register_blueprint(countries_bp)
    app.register_blueprint(cities_bp)
    app.register_blueprint(places_bp)
    app.register_blueprint(amenities_bp)
    app.register_blueprint(reviews_bp)
