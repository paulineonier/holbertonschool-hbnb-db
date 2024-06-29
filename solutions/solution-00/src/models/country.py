"""
Country related functionality
"""

from src import db  # Importez db depuis votre package source
from src.models.base import Base


class Country(db.Model):
    """
    Country representation

    This class represents a Country in the database.
    """

    __tablename__ = 'countries'  # Nom de la table dans la base de données

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    code = db.Column(db.String(2), nullable=False)

    def __init__(self, name: str, code: str) -> None:
        """Initialisation d'un pays"""
        self.name = name
        self.code = code

    def __repr__(self) -> str:
        """Représentation sous forme de chaîne du pays"""
        return f"<Country {self.code} ({self.name})>"

    def to_dict(self) -> dict:
        """Retourne la représentation de l'objet sous forme de dictionnaire"""
        return {
            "name": self.name,
            "code": self.code,
        }

    @staticmethod
    def get_all() -> list["Country"]:
        """Récupère tous les pays de la base de données"""
        return Country.query.all()

    @staticmethod
    def get(code: str) -> "Country | None":
        """Récupère un pays par son code"""
        return Country.query.filter_by(code=code).first()

    @staticmethod
    def create(name: str, code: str) -> "Country":
        """Crée un nouveau pays"""
        new_country = Country(name=name, code=code)

        db.session.add(new_country)
        db.session.commit()

        return new_country
