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


#EMPEZAMOS A TRABAJAR DESDE ACA

#este endpoint nos permite traer la informacion de todos los users
@app.route('/user', methods=['GET'])
def handle_hello():
    allusers = User.query.all()
    results = list(map(lambda item: item.serialize(),allusers))
    return jsonify(results), 200


#aca traemos la informacion de un solo user    
@app.route('/user/<int:user_id>', methods=['GET'])
def handle_singleuser(user_id):
    one_user = User.query.filter_by(id=user_id).first()
    print(one_user)
    if one_user is None:
        return jsonify({"msg":"usuario no existente"}), 404
    else:
        return jsonify(one_user.serialize()), 200

#aca traemos la informacion de un solo character    
@app.route('/characters/<int:character_id>', methods=['GET'])
def handle_one_character(character_id):
    one_character = Character.query.filter_by(id=character_id).first()
    if one_character is None:
        return jsonify({"msg":"planeta no existente"}), 404
    else:
        return jsonify(one_character.serialize()), 200
        
#aca traemos la informacion de un solo planet    
@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_one_planet(planet_id):
    one_planet = Planet.query.filter_by(id=planet_id).first()
    if one_planet is None:
        return jsonify({"msg":"planeta no existente"}), 404
    else:
        return jsonify(one_planet.serialize()), 200        

#aca traemos la informacion de un solo vehicle    
@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def handle_one_vehicle(vehicle_id):
    one_vehicle = Vehicle.query.filter_by(id=vehicle_id).first()
    if one_vehicle is None:
        return jsonify({"msg":"vehiculo no existente"}), 404
    else:
        return jsonify(one_vehicle.serialize()), 200        



#creamos un usuario si no no podiamos hacer lo de favorites, porque para darle favoritos ena pagina debemos tener una cuenta
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

#aca traemos a todos los favorites
@app.route('/favourites', methods=['GET'])
def handle_favourites():
    all_favourites = Favourite.query.all()
    results = list(map(lambda item: item.serialize(),all_favourites))
    return jsonify(results), 200 
        
# POST: ACTUALIZA LA INFORMACION        
@app.route('/favourites/characters/<int:user_ID>/<int:character_ID>', methods=['POST'])
def add_favourite_character(user_ID, character_ID):
    # controla que exista el usuario, va a buscar usuario existe              #true #
    one_user = User.query.filter_by(id=user_ID).first()
    print(one_user)
    #Si existe el usuario #si la variable anazlizada tiene algo ya se va a asumir que la condicion va a dar true por default de lo contrario pasa al else que asume que es null
    if one_user:
        print("estoy en el if")
    #     # esto controla que existan los personajes, si no existe el personaje lo agrega  lo de la linea comprueba que existe hace todo lo que no queremos
        character = Favourite.query.filter_by(id=character_ID).first()
        print(character)
    #     # si character se cumple entonces se ejecuta el mensaje
        if character:
            response_body = {"msg": "El personaje seleccionado ya está en la lista de favoritos"}
            return jsonify(response_body), 404
    #     # aca se va a retornar todo lo que queremos
        else:
            print("hay que crear")
            #                    propiedad: mencion que hacemos a la tabla, el valor: 
            # new_character = Favourite(user_id=2, character_id=1) 
            new_character = Favourite(user_id=user_ID, character_id=character_ID) 
            db.session.add(new_character)
            db.session.commit()
            response_body = {"msg":"Se ha agregado el personaje a Favoritos"}
            # favourite_character = Favourite.query.filter_by(id=character_ID).first()
            # print(favourite_character)
            return jsonify(response_body), 200 
    else:
        response_body = {"msg":"El usuario no existe"}
        return jsonify(response_body), 404
    return jsonify("ok"), 200        

@app.route('/favourites/planets/<int:user_ID>/<int:planet_ID>', methods=['POST'])
def add_favourite_planet(user_ID, planet_ID):
    # controla que exista el usuario, va a buscar usuario existe              #true #
    one_user = User.query.filter_by(id=user_ID).first()
    # print(one_user)
    #Si existe el usuario #si la variable anazlizada tiene algo ya se va a asumir que la condicion va a dar true por default de lo contrario pasa al else que asume que es null
    if one_user:
        # print("estoy en el if")
    #     # esto controla que existan los personajes, si no existe el personaje lo agrega  lo de la linea comprueba que existe hace todo lo que no queremos
        planet = Favourite.query.filter_by(id=planet_ID).first()
        print(planet)
        # print(character)
    #     # si character se cumple entonces se ejecuta el mensaje
        if planet:
            response_body = {"msg": "El planeta seleccionado ya está en la lista de favoritos"}
            return jsonify(response_body), 404
    #     # aca se va a retornar todo lo que queremos
        else:
            # print("hay que crear")
            #                    propiedad: mencion que hacemos a la tabla, el valor: 
            # new_character = Favourite(user_id=2, character_id=1) 
            new_planet = Favourite(user_id=user_ID, planet_id=planet_ID) 
            db.session.add(new_planet)
            db.session.commit()
            response_body = {"msg":"Se ha agregado el planeta a Favoritos"}
            # favourite_planet = Favourite.query.filter_by(id=character_ID).first()
            # print(favourite_planet)
            return jsonify(response_body), 200 
    else:
        response_body = {"msg":"El usuario no existe"}
        return jsonify(response_body), 404
    # return jsonify("ok"), 200        


    	
        




#ACA TERMINAMOS DE TRABAJAR


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
