"""
This module contains the routes for the users endpoints.
"""

from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.controllers.users import (
    create_user,
    delete_user,
    get_user_by_id,
    get_users,
    update_user,
)
from src.models.user import User

users_bp = Blueprint("users", __name__, url_prefix="/users")

# Routes sans authentification
users_bp.route("/", methods=["POST"])(create_user)

# Routes avec authentification
@users_bp.route("/", methods=["GET"])
@jwt_required()
def secure_get_users():
    return get_users()

@users_bp.route("/<user_id>", methods=["GET"])
@jwt_required()
def secure_get_user_by_id(user_id):
    return get_user_by_id(user_id)

@users_bp.route("/<user_id>", methods=["PUT"])
@jwt_required()
def secure_update_user(user_id):
    return update_user(user_id)

@users_bp.route("/<user_id>", methods=["DELETE"])
@jwt_required()
def secure_delete_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user.is_admin:
        return {"msg": "Admin access required"}, 403

    return delete_user(user_id)
