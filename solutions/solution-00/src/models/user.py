"""
User related functionality
"""

from src import db  
# Importez db depuis votre package source


class User(db.Model):
    """User representation"""

    __tablename__ = 'users'  
    # Nom de la table dans la base de données

    id = db.Column(db.String(36), primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    def __init__(self, email: str, first_name: str, last_name: str, **kwargs):
        """Initialisation d'un utilisateur"""
        super().__init__(**kwargs)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self) -> str:
        """Représentation sous forme de chaîne de l'utilisateur"""
        return f"<User {self.id} ({self.email})>"

    def to_dict(self) -> dict:
        """Retourne la représentation de l'objet sous forme de dictionnaire"""
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(user_data: dict) -> "User":
        """Crée un nouvel utilisateur"""
        new_user = User(**user_data)

        db.session.add(new_user)
        db.session.commit()

        return new_user

    @staticmethod
    def update(user_id: str, data: dict) -> "User | None":
        """Met à jour un utilisateur existant"""
        user = User.query.get(user_id)

        if not user:
            return None

        if "email" in data:
            user.email = data["email"]
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]

        db.session.commit()

        return user
