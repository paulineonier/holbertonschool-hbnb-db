from flask import request, jsonify
from src.models.user import User
from src import db

def create_user():
    """Create a new user"""
    data = request.get_json()
    new_user = User.create(data)
    return jsonify(new_user.to_dict()), 201

def get_users():
    """Get all users"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

def get_user_by_id(user_id):
    """Get user by ID"""
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg": "User not found"}), 404
    return jsonify(user.to_dict()), 200

def update_user(user_id):
    """Update an existing user"""
    data = request.get_json()
    updated_user = User.update(user_id, data)
    if updated_user is None:
        return jsonify({"msg": "User not found"}), 404
    return jsonify(updated_user.to_dict()), 200

def delete_user(user_id):
    """Delete a user"""
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted"}), 200
