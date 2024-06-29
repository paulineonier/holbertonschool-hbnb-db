from flask import request, jsonify
from src.models.city import City
from src import db

def create_city():
    """Create a new city"""
    data = request.get_json()
    new_city = City.create(data)
    return jsonify(new_city.to_dict()), 201

def get_cities():
    """Get all cities"""
    cities = City.query.all()
    return jsonify([city.to_dict() for city in cities]), 200

def get_city_by_id(city_id):
    """Get city by ID"""
    city = City.query.get(city_id)
    if city is None:
        return jsonify({"msg": "City not found"}), 404
    return jsonify(city.to_dict()), 200

def update_city(city_id):
    """Update an existing city"""
    data = request.get_json()
    updated_city = City.update(city_id, data)
    if updated_city is None:
        return jsonify({"msg": "City not found"}), 404
    return jsonify(updated_city.to_dict()), 200

def delete_city(city_id):
    """Delete a city"""
    city = City.query.get(city_id)
    if city is None:
        return jsonify({"msg": "City not found"}), 404

    db.session.delete(city)
    db.session.commit()
    return jsonify({"msg": "City deleted"}), 200
