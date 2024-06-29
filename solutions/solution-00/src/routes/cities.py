"""
This module contains the routes for the cities blueprint
"""

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.controllers.cities import (
    create_city,
    delete_city,
    get_city_by_id,
    get_cities,
    update_city,
)
from src.models.user import User

cities_bp = Blueprint("cities", __name__, url_prefix="/cities")

# Routes sans authentification
cities_bp.route("/", methods=["POST"])(create_city)

# Routes avec authentification
@cities_bp.route("/", methods=["GET"])
@jwt_required()
def secure_get_cities():
    return get_cities()

@cities_bp.route("/<city_id>", methods=["GET"])
@jwt_required()
def secure_get_city_by_id(city_id):
    return get_city_by_id(city_id)

@cities_bp.route("/<city_id>", methods=["PUT"])
@jwt_required()
def secure_update_city(city_id):
    return update_city(city_id)

@cities_bp.route("/<city_id>", methods=["DELETE"])
@jwt_required()
def secure_delete_city(city_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user.is_admin:
        return jsonify({"msg": "Admin access required"}), 403

    return delete_city(city_id)
