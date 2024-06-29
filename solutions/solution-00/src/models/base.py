""" Abstract base class for all models """

from datetime import datetime
from typing import Any, Optional
import uuid
from abc import ABC, abstractmethod
from src import db

class Base:
    """
    Base Interface for all models
    """

    __abstract__ = True  # This makes SQLAlchemy treat this class as abstract

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs) -> None:
        """
        Base class constructor
        If kwargs are provided, set them as attributes
        """
        super().__init__(**kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def get(cls, id) -> "Any | None":
        """
        This is a common method to get a specific object
        of a class by its id
        """
        return cls.query.get(id)

    @classmethod
    def get_all(cls) -> list["Any"]:
        """
        This is a common method to get all objects of a class
        """
        return cls.query.all()

    @classmethod
    def delete(cls, id) -> bool:
        """
        This is a common method to delete a specific
        object of a class by its id
        """
        obj = cls.get(id)
        if not obj:
            return False
        db.session.delete(obj)
        db.session.commit()
        return True

    @abstractmethod
    def to_dict(self) -> dict:
        """Returns the dictionary representation of the object"""

    @staticmethod
    @abstractmethod
    def create(data: dict) -> Any:
        """Creates a new object of the class"""

    @staticmethod
    @abstractmethod
    def update(entity_id: str, data: dict) -> Any | None:
        """Updates an object of the class"""
