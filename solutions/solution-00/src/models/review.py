"""
Review related functionality
"""
from src import db
from src.models.user import User
from src.models.place import Place


class Review(db.Model):
    """Review representation"""

    __tablename__ = 'reviews'

    id = db.Column(db.String(36), primary_key=True)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    place = db.relationship('Place', backref=db.backref('reviews', lazy=True))

    def __init__(self, place_id: str, user_id: str, comment: str, rating: float, **kwargs) -> None:
        """Initialisation d'une critique"""
        super().__init__(**kwargs)
        self.place_id = place_id
        self.user_id = user_id
        self.comment = comment
        self.rating = rating

    def __repr__(self):
        return f"<Review {self.id}>"

    def to_dict(self) -> dict:
        """Retourne la représentation de l'objet sous forme de dictionnaire"""
        return {
            "id": self.id,
            "place_id": self.place_id,
            "user_id": self.user_id,
            "comment": self.comment,
            "rating": self.rating,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


    @staticmethod
    def create(data: dict) -> "Review":
        """Crée une nouvelle critique"""
        try:
            new_review = Review(**data)
            db.session.add(new_review)
            db.session.commit()
            return new_review
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update(review_id: str, data: dict) -> "Review | None":
        """Met à jour une critique existante"""
        try:
            review = Review.query.get(review_id)
            if not review:
                return None
            for key, value in data.items():
                setattr(review, key, value)
            db.session.commit()
            return review
        except Exception as e:
            db.session.rollback()
            raise e
