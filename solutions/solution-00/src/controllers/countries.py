from src.models.country import Country

def get_countries():
    """Get all countries"""
    countries = Country.query.all()
    return jsonify([country.to_dict() for country in countries]), 200

def get_country_by_code(code):
    """Get country by code"""
    country = Country.query.filter_by(code=code).first()
    if country is None:
        return jsonify({"msg": "Country not found"}), 404
    return jsonify(country.to_dict()), 200

def get_country_cities(code):
    """Get cities in a country by code"""
    country = Country.query.filter_by(code=code).first()
    if country is None:
        return jsonify({"msg": "Country not found"}), 404
    return jsonify([city.to_dict() for city in country.cities]), 200
