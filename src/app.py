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
    pass


#GET single planet


#GET all vehicles


#GET single vehicle


#GET all users


#GET one user's favorites



#POST favorite planet


#POST favorite character
@app.route("/favorite/characters", methods=["POST"])
def add_favorite_person():


    #retrieve info found in the body portion of the client request
    data = request.get_json()
    new_favorite_character = Favorites(user_id = data["user_id"], character_id = data["character_id"])
    db.session.add(new_favorite_character)
    db.session.commit()

    return jsonify("Your favortie was added."), 200
    


#POST favorite vehicle



#DELETE favorite planet


#DELETE favorite character


#DELETE favorite vehicle



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
