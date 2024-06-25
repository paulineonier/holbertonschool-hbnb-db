"""
Place related functionality
"""

from src import db  # Importez db depuis votre package source
from src.models.city import City
from src.models.base import Base

class Place(Base):
    """Place representation"""

    __tablename__ = 'places'  # Nom de la table dans la base de données

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    host_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    city_id = db.Column(db.String(36), db.ForeignKey('cities.id'), nullable=False)
    price_per_night = db.Column(db.Integer, nullable=False)
    number_of_rooms = db.Column(db.Integer, nullable=False)
    number_of_bathrooms = db.Column(db.Integer, nullable=False)
    max_guests = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    city = db.relationship('City', backref=db.backref('places', lazy=True))
    host = db.relationship('User', backref=db.backref('places', lazy=True))

    def __init__(self, data: dict | None = None, **kwargs) -> None:
        """Initialisation d'un lieu"""
        super().__init__(**kwargs)

        if data is None:
            return

        self.name = data.get("name", "")
        self.description = data.get("description", "")
        self.address = data.get("address", "")
        self.latitude = float(data.get("latitude", 0.0))
        self.longitude = float(data.get("longitude", 0.0))
        self.host_id = data["host_id"]
        self.city_id = data["city_id"]
        self.price_per_night = int(data.get("price_per_night", 0))
        self.number_of_rooms = int(data.get("number_of_rooms", 0))
        self.number_of_bathrooms = int(data.get("number_of_bathrooms", 0))
        self.max_guests = int(data.get("max_guests", 0))

    def __repr__(self) -> str:
        """Représentation sous forme de chaîne du lieu"""
        return f"<Place {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Retourne la représentation de l'objet sous forme de dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "city_id": self.city_id,
            "host_id": self.host_id,
            "price_per_night": self.price_per_night,
            "number_of_rooms": self.number_of_rooms,
            "number_of_bathrooms": self.number_of_bathrooms,
            "max_guests": self.max_guests,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "Place":
        """Crée un nouveau lieu"""
        new_place = Place(data=data)

        db.session.add(new_place)
        db.session.commit()

        return new_place

    @staticmethod
    def update(place_id: str, data: dict) -> "Place | None":
        """Met à jour un lieu existant"""
        place = Place.query.get(place_id)

        if not place:
            return None

        for key, value in data.items():
            setattr(place, key, value)

        db.session.commit()

        return place
