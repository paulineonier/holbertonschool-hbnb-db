"""
This module contains the routes for the amenities blueprint
"""

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.controllers.amenities import (
    create_amenity,
    delete_amenity,
    get_amenity_by_id,
    get_amenities,
    update_amenity,
)
from src.models.user import User

amenities_bp = Blueprint("amenities", __name__, url_prefix="/amenities")

# Routes sans authentification
amenities_bp.route("/", methods=["POST"])(create_amenity)

# Routes avec authentification
@amenities_bp.route("/", methods=["GET"])
@jwt_required()
def secure_get_amenities():
    return get_amenities()

@amenities_bp.route("/<amenity_id>", methods=["GET"])
@jwt_required()
def secure_get_amenity_by_id(amenity_id):
    return get_amenity_by_id(amenity_id)

@amenities_bp.route("/<amenity_id>", methods=["PUT"])
@jwt_required()
def secure_update_amenity(amenity_id):
    return update_amenity(amenity_id)

@amenities_bp.route("/<amenity_id>", methods=["DELETE"])
@jwt_required()
def secure_delete_amenity(amenity_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user.is_admin:
        return jsonify({"msg": "Admin access required"}), 403

    return delete_amenity(amenity_id)
