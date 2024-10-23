from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    firstname = db.Column(db.String(120))
    lastname = db.Column(db.String(120))
    favorites = db.relationship('Favorites', back_populates='users')


    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
        }
    
    def ser_favorites(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "favorites": self.favorites
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    eye_color = db.Column(db.String(20))
    height_cm = db.Column(db.Integer)
    birth_year = db.Column(db.String(20))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "height": self.height_cm,
            "eye color": self.eye_color
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    climate = db.Column(db.String(50))
    diameter = db.Column(db.Integer)
    population = db.Column(db.Integer)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "population": self.population,
            "climate": self.climate
        }

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    users = db.relationship('User', back_populates='favorites')
    characters = db.relationship('Character')
    planets = db.relationship('Planet')

    def serialize(self):
        return {
            "user": self.user_id,
            "character": self.character_id,
            "planet": self.planet_id,
        }
    