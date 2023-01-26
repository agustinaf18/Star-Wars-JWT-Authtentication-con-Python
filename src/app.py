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
from models import db, User, Character, Planet, Vehicle, Favourite
import json
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


#empezamos a trabajar desde aca
#este endpoint nos permite traer la informacion de todos los users
@app.route('/user', methods=['GET'])
def handle_hello():
    allusers = User.query.all()
    results = list(map(lambda item: item.serialize(),allusers))
    return jsonify(results), 200

#aca traemos la informacion de un solo character    

@app.route('/user/<int:user_id>', methods=['GET'])
def handle_singleuser(user_id):
    one_user = User.query.filter_by(id=user_id).first()
    print(one_user)
    if one_user is None:
        return jsonify({"msg":"usuario no existente"}), 404
    else:
        return jsonify(one_user.serialize()), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def handle_one_character(character_id):
    one_character = Character.query.filter_by(id=character_id).first()
    if one_character is None:
        return jsonify({"msg":"planeta no existente"}), 404
    else:
        return jsonify(one_character.serialize()), 200



@app.route('/user/', methods=['POST'])
def add_user():
    request_body = request.data  #es la informacion que viene del postman la que viene del front end
    decoded_object = json.loads(request_body)  # traduce la informacion, lo pasa a json 
    print(decoded_object) # hace que podamos ver la informacion de manera que la necesitamos
    get_email = User.query.filter_by(email=decoded_object["email"]).first()
    if get_email is None:
            new_user = User(user_name=decoded_object["user_name"], email=decoded_object["email"], password=decoded_object["password"])
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"msg":"usuario creado exitosamente"}), 200
    else: 
        return jsonify({"msg":"el email ya existe"}), 400 

#aca traemos a todos los characters
@app.route('/characters', methods=['GET'])
def handle_characters():
    all_characters = Character.query.all()
    results = list(map(lambda item: item.serialize(),all_characters))
    return jsonify(results), 200          

#aca traemos a todos los planets
@app.route('/planets', methods=['GET'])
def handle_planets():
    all_planets = Planet.query.all()
    results = list(map(lambda item: item.serialize(),all_planets))
    return jsonify(results), 200    

#aca traemos a todos los vehicles
@app.route('/vehicles', methods=['GET'])
def handle_vehicles():
    all_vehicles = Vehicle.query.all()
    results = list(map(lambda item: item.serialize(),all_vehicles))
    return jsonify(results), 200   

#aca traemos a todos los vehicles
@app.route('/favourites', methods=['GET'])
def handle_favourites():
    all_favourites = Favourite.query.all()
    results = list(map(lambda item: item.serialize(),all_favourites))
    return jsonify(results), 200 
        
@app.route('/favourites/characters/<int:user_id>/<int:character_id>', methods=['POST'])
def add_favourite_character(user_id, character_id):
    one_user = User.query.filter_by(id=user_id).first()
    if one_user is None:
        
        




#aca terminamos de trabajar


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
