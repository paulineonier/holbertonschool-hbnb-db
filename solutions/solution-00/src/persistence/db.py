"""
  Now is easy to implement the database repository. The DBRepository
  should implement the Repository (Storage) interface and the methods defined
  in the abstract class Storage.

  The methods to implement are:
    - get_all
    - get
    - save
    - update
    - delete
    - reload (which can be empty)
"""
from src.models.base import Base
from src.persistence.repository import Repository
from src import db  # Importer SQLAlchemy instance de src/__init__.py

class DBRepository(Repository):
    """Implementation of the Repository interface for a database using SQLAlchemy."""

    def __init__(self) -> None:
        """Initialize the DBRepository."""
        self.session = db.session

    def get_all(self, model_name: str) -> list:
        """Get all records of a given model."""
        model_class = Base._decl_class_registry.get(model_name, None)
        if model_class is None:
            raise ValueError(f"Model {model_name} does not exist.")
        return self.session.query(model_class).all()

    def get(self, model_name: str, obj_id: str) -> Base | None:
        """Get a single record by its ID."""
        model_class = Base._decl_class_registry.get(model_name, None)
        if model_class is None:
            raise ValueError(f"Model {model_name} does not exist.")
        return self.session.query(model_class).get(obj_id)

    def save(self, obj: Base) -> None:
        """Save a new record to database."""
        self.session.add(obj)
        self.session.commit()

    def update(self, obj: Base) -> Base | None:
        """Update an existing record in the database."""
        self.session.merge(obj)
        self.session.commit()
        return obj

    def delete(self, obj: Base) -> bool:
        """Delete a record frm the dtabase."""
        self.session.delete(obj)
        self.session.commit()
        return True

    def reload(self) -> None:
        """Reload the database session."""
        self.session.expire_all()
