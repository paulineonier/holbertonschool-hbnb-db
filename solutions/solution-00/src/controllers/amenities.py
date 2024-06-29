from flask import request, jsonify
from src.models.amenity import Amenity
from src import db

def create_amenity():
    """Create a new amenity"""
    data = request.get_json()
    new_amenity = Amenity.create(data)
    return jsonify(new_amenity.to_dict()), 201

def get_amenities():
    """Get all amenities"""
    amenities = Amenity.query.all()
    return jsonify([amenity.to_dict() for amenity in amenities]), 200

def get_amenity_by_id(amenity_id):
    """Get amenity by ID"""
    amenity = Amenity.query.get(amenity_id)
    if amenity is None:
        return jsonify({"msg": "Amenity not found"}), 404
    return jsonify(amenity.to_dict()), 200

def update_amenity(amenity_id):
    """Update an existing amenity"""
    data = request.get_json()
    updated_amenity = Amenity.update(amenity_id, data)
    if updated_amenity is None:
        return jsonify({"msg": "Amenity not found"}), 404
    return jsonify(updated_amenity.to_dict()), 200

def delete_amenity(amenity_id):
    """Delete an amenity"""
    amenity = Amenity.query.get(amenity_id)
    if amenity is None:
        return jsonify({"msg": "Amenity not found"}), 404

    db.session.delete(amenity)
    db.session.commit()
    return jsonify({"msg": "Amenity deleted"}), 200
