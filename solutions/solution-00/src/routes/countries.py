"""
This module contains the routes for the countries endpoint
"""

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from src.controllers.countries import (
    get_countries,
    get_country_by_code,
    get_country_cities,
)

countries_bp = Blueprint("countries", __name__, url_prefix="/countries")

@countries_bp.route("/", methods=["GET"])
@jwt_required()
def secure_get_countries():
    return get_countries()

@countries_bp.route("/<code>", methods=["GET"])
@jwt_required()
def secure_get_country_by_code(code):
    return get_country_by_code(code)

@countries_bp.route("/<code>/cities", methods=["GET"])
@jwt_required()
def secure_get_country_cities(code):
    return get_country_cities(code)
