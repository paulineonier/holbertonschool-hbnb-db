"""
This module contains the routes for the places blueprint
"""

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from src.controllers.places import (
    create_place,
    delete_place,
    get_place_by_id,
    get_places,
    update_place,
)

places_bp = Blueprint("places", __name__, url_prefix="/places")

@places_bp.route("/", methods=["GET"])
@jwt_required()
def secure_get_places():
    return get_places()

@places_bp.route("/", methods=["POST"])
@jwt_required()
def secure_create_place():
    return create_place()

@places_bp.route("/<place_id>", methods=["GET"])
@jwt_required()
def secure_get_place_by_id(place_id):
    return get_place_by_id(place_id)

@places_bp.route("/<place_id>", methods=["PUT"])
@jwt_required()
def secure_update_place(place_id):
    return update_place(place_id)

@places_bp.route("/<place_id>", methods=["DELETE"])
@jwt_required()
def secure_delete_place(place_id):
    return delete_place(place_id)
