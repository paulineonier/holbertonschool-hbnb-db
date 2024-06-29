"""
City related functionality
"""

from src.extensions import db
from src.models.base import Base
from src.models.country import Country


class City(Base):
    """City representation"""

    __tablename__ = 'cities'  # Nom de la table dans la base de données

    name = db.Column(db.String(128), nullable=False)
    country_code = db.Column(db.String(2), db.ForeignKey('countries.code'), nullable=False)

    # Définissez la relation avec Country si nécessaire
    country = db.relationship('Country', backref='cities')

    def __init__(self, name: str, country_code: str, **kw) -> None:
        """Initialisation d'une ville"""
        super().__init__(**kw)

        self.name = name
        self.country_code = country_code

    def __repr__(self) -> str:
        """Représentation sous forme de chaîne de la ville"""
        return f"<City {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Retourne la représentation de l'objet sous forme de dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "country_code": self.country_code,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "City":
        """Crée une nouvelle ville"""
        country = Country.query.filter_by(code=data["country_code"]).first()

        if not country:
            raise ValueError("Country not found")

        city = City(**data)

        db.session.add(city)
        db.session.commit()

        return city

    @staticmethod
    def update(city_id: str, data: dict) -> "City":
        """Met à jour une ville existante"""
        city = City.query.get(city_id)

        if not city:
            raise ValueError("City not found")

        for key, value in data.items():
            setattr(city, key, value)

        db.session.commit()

        return city
