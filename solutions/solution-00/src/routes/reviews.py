"""
This module contains the routes for the reviews blueprint
"""

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from src.controllers.reviews import (
    create_review,
    delete_review,
    get_reviews_from_place,
    get_reviews_from_user,
    get_review_by_id,
    get_reviews,
    update_review,
)

reviews_bp = Blueprint("reviews", __name__)

@reviews_bp.route("/places/<place_id>/reviews", methods=["POST"])
@jwt_required()
def secure_create_review(place_id):
    return create_review(place_id)

@reviews_bp.route("/places/<place_id>/reviews", methods=["GET"])
@jwt_required(optional=True)
def secure_get_reviews_from_place(place_id):
    return get_reviews_from_place(place_id)

@reviews_bp.route("/users/<user_id>/reviews", methods=["GET"])
@jwt_required(optional=True)
def secure_get_reviews_from_user(user_id):
    return get_reviews_from_user(user_id)

@reviews_bp.route("/reviews", methods=["GET"])
@jwt_required(optional=True)
def secure_get_reviews():
    return get_reviews()

@reviews_bp.route("/reviews/<review_id>", methods=["GET"])
@jwt_required()
def secure_get_review_by_id(review_id):
    return get_review_by_id(review_id)

@reviews_bp.route("/reviews/<review_id>", methods=["PUT"])
@jwt_required()
def secure_update_review(review_id):
    return update_review(review_id)

@reviews_bp.route("/reviews/<review_id>", methods=["DELETE"])
@jwt_required()
def secure_delete_review(review_id):
    return delete_review(review_id)
