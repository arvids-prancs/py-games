from app import db


class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title_lat = db.Column(db.String(100), nullable=False)
