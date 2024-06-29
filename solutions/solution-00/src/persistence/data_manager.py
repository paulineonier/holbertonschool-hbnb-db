from src.persistence import db

class DataManager:
    def __init__(self, use_database=False):
        self.use_database = use_database

    def save(self, entity):
        if self.use_database:
            db.session.add(entity)
            db.session.commit()
        else:
            # Logique de sauvegarde dans le système de fichiers
            pass
    
    def get(self, entity_id):
        if self.use_database:
            return db.session.query(Entity).filter_by(id=entity_id).first()
        else:
            # Logique de récupération depuis le système de fichiers
            pass
    
    def update(self, entity):
        if self.use_database:
            db.session.commit()  # Suppose que l'entité a déjà été modifiée
        else:
            # Logique de mise à jour dans le système de fichiers
            pass
    
    def delete(self, entity):
        if self.use_database:
            db.session.delete(entity)
            db.session.commit()
        else:
            # Logique de suppression dans le système de fichiers
            pass
