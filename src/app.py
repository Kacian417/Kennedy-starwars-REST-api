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
from models import db, User, Character, Planet, Vehicle, Favorites
#from models import Person

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

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

#GET all characters (people) and specific characters via routes
@app.route("/characters", methods=["GET"])
def get_all_characters():
    #query the database to get all the starwars characters
    all_characters = Character.query.all()

    if all_characters is None:
        return jsonify("No records found."), 404
    else:
        all_characters = list(map(lambda x: x.serialize(), all_characters))
        return jsonify(all_characters), 200


@app.route("/characters/<int:character_id>", methods=["GET"])
def get_character(character_id):
    single_character = Character.query.get(character_id)

    if single_character is None:
        raise APIException(f'Character ID {character_id} is not found!', status_code=404)
    
    single_character = single_character.serialize()
    return jsonify(single_character), 200

#Planets
@app.route("/planets", methods=["GET"])
def get_all_planets():
    all_planets = Planet.query.all()

    if not all_planets:  # This checks if the list is empty
        return jsonify("No records found."), 404
    else:
        all_planets = list(map(lambda x: x.serialize(), all_planets))
        return jsonify(all_planets), 200


#GET single planet
@app.route("/planets/<int:planet_id>", methods=["GET"])
def get_planet(planet_id):
    single_planet = Planet.query.get(planet_id)

    if single_planet is None:
        raise APIException(f'Planet ID {planet_id} is not found!', status_code=404)
    
    single_planet = single_planet.serialize()
    return jsonify(single_planet), 200

#GET all vehicles
@app.route("/vehicles", methods=["GET"])
def get_all_vehicles():
    all_vehicles = Vehicle.query.all()

    if not all_vehicles:
        return jsonify("No records found."), 404
    else:
        all_vehicles = list(map(lambda x: x.serialize(), all_vehicles))
        return jsonify(all_vehicles), 200

#GET single vehicle
@app.route("/vehicles/<int:vehicle_id>", methods=["GET"])
def get_vehicle(vehicle_id):
    single_vehicle = Vehicle.query.get(vehicle_id)

    if single_vehicle is None:
        raise APIException(f'Vehicle ID {vehicle_id} is not found!', status_code=404)
    
    single_vehicle = single_vehicle.serialize()
    return jsonify(single_vehicle), 200

#GET all users
@app.route("/users", methods=["GET"])
def get_all_users():
    all_users = User.query.all()

    if all_users is None:
        return jsonify("No records found."), 404
    else:
        all_users = list(map(lambda x: x.serialize(), all_users))
        return jsonify(all_users), 200

#GET one user's favorites
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user_favorites(user_id):
    single_user = User.query.get(user_id)

    if single_user is None:
        raise APIException(f'User ID {user_id} is not found!', status_code=404)
    
    single_user = single_user.serialize()
    return jsonify(single_user), 200


#POST favorite planet
@app.route("/favorite/planets", methods=["POST"])
def add_favorite_planet():

    data = request.get_json()
    new_favorite_planet = Favorites(user_id = data["user_id"], planet_id = data["planet_id"])
    db.session.add(new_favorite_planet)
    db.session.commit()

    return jsonify("Your favorite was added."), 200

#POST favorite character
@app.route("/favorite/characters", methods=["POST"])
def add_favorite_person():


    #retrieve info found in the body portion of the client request
    data = request.get_json()
    new_favorite_character = Favorites(user_id = data["user_id"], character_id = data["character_id"])
    db.session.add(new_favorite_character)
    db.session.commit()

    return jsonify("Your favorite was added."), 200
    
#POST favorite vehicle
@app.route("/favorites/vehicles", methods=["POST"])
def add_favorite_vehicle():

    data = request.get_json()
    new_favorite_vehicle = Favorites(user_id = data["user_id"], vehicle_id = data["vehicle_id"])
    db.session.add(new_favorite_vehicle)
    db.session.commit()

    return jsonify("Your favorite was added."), 200


#DELETE favorite planet
@app.route("/favorites/planets/<int:planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    planet = Favorites.query.get(planet_id)
    
    if not planet:
        return jsonify({"message": "Favorite planet not found"}), 404

    db.session.delete(planet)
    db.session.commit()

    return jsonify({"message": f"Favorite planet {planet_id} was successfully deleted"}), 200

#DELETE favorite character
@app.route("/favorites/characters/<int:character_id>", methods=["DELETE"])
def delete_character(character_id):
    character = Favorites.query.get(character_id)
    
    if not character:
        return jsonify({"message": "Favorite character not found"}), 404

    db.session.delete(character)
    db.session.commit()

    return jsonify({"message": f"Favorite character {character_id} was successfully deleted"}), 200

#DELETE favorite vehicle
@app.route("/favorites/vehicles/<int:vehicle_id>", methods=["DELETE"])
def delete_vehicle(vehicle_id):
    vehicle = Favorites.query.get(vehicle_id)
    
    if not vehicle:
        return jsonify({"message": "Favorite vehicle not found"}), 404

    db.session.delete(vehicle)
    db.session.commit()

    return jsonify({"message": f"Favorite vehicle {vehicle_id} was successfully deleted"}), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
