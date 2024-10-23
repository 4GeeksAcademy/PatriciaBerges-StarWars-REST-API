"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorites

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_people():
    people = Character.query.all()
    response_body = [character.serialize() for character in people]
    return jsonify(response_body), 200

@app.route('/people/<int:id>', methods=['GET'])
def get_character(id):
    character = Character.query.get(id)
    if not character:
        return jsonify({"error": "Character id doesn't exist"}), 404
    response_body = character.serialize()
    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    response_body = [planet.serialize() for planet in planets]
    return jsonify(response_body), 200

@app.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):
    planet = Planet.query.get(id)
    if not planet:
        return jsonify({"error": "Planet id doesn't exist"}), 404
    response_body = planet.serialize()
    return jsonify(response_body), 200

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    response_body = [user.serialize() for user in users]
    return jsonify(response_body), 200

@app.route('/users/favorites', methods=['GET'])
def get_favorites():
    favs = Favorites.query.filter(Favorites.user_id == 1).all()
    response_body = [fav.serialize() for fav in favs]
    return jsonify(response_body), 200

@app.route('/favorite/planet/<int:id>', methods=['POST'])
def add_fav_planet(id):
    planet = Planet.query.get(id)
    if not planet:
        return jsonify({"error": "Planet id doesn't exist"}), 404
    fav_planet = Favorites()
    fav_planet.user_id = 1
    fav_planet.planet_id = id
    db.session.add(fav_planet)
    db.session.commit()
    response_body = fav_planet.serialize()
    return jsonify(response_body), 200

@app.route('/favorite/people/<int:id>', methods=['POST'])
def add_fav_character(id):
    character = Character.query.get(id)
    if not character:
        return jsonify({"error": "Character id doesn't exist"}), 404
    fav_char = Favorites()
    fav_char.user_id = 1
    fav_char.character_id = id
    db.session.add(fav_char)
    db.session.commit()
    response_body = fav_char.serialize()
    return jsonify(response_body), 200

@app.route('/favorite/planet/<int:id>', methods=['DELETE'])
def delete_planet(id):
    planet = Favorites.query.filter(Favorites.user_id == 1, Favorites.planet_id == id).first()
    if not planet:
        return jsonify({"error": "Planet is not in user favorites"}), 404
    db.session.delete(planet)
    db.session.commit()
    return jsonify({"Success": "Deleted planet from favorites"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
