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
from models import db, User, Vehicle, People, Planet, Favorite
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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
def get_user():

    users = User.query.all()

    return jsonify([
        user.serialize() for user in users
    ]), 200


@app.route('/favorite/<int:user_id>', methods=['GET'])
def get_favorite(user_id):

    favorites = Favorite.query.filter_by(user_id=user_id).all()

    return jsonify([
        favorite.serialize() for favorite in favorites
    ]), 200


@app.route('/people', methods=['GET'])
def get_people():

    peoples = People.query.all()

    return jsonify([
        people.serialize() for people in peoples
    ]), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_id(people_id):

    people = People.query.get(people_id)

    if people is None:
        return jsonify({"error": "Person not found"}), 404

    return jsonify(people.serialize()), 200


@app.route('/planet', methods=['GET'])
def get_planet():
    planets = Planet.query.all()

    return jsonify([
        planet.serialize() for planet in planets
    ]), 200


@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet_id(planet_id):
    planet = Planet.query.get(planet_id)

    if planet is None:
        return jsonify({"error": "planet not found"}), 404

    return jsonify(planet.serialize()), 200


@app.route('/vehicle', methods=['GET'])
def get_vehicle():
    vehicles = Vehicle.query.all()

    return jsonify([
        vehicle.serialize() for vehicle in vehicles
    ]), 200


@app.route('/vehicle/<int:vehicle_id>', methods=['GET'])
def get_vehicle_id(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)

    if vehicle is None:
        return jsonify({"error": "Vehicle not found"}), 404

    return jsonify(vehicle.serialize()), 200


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()

    required_fields = ['email', 'password']
    for field in required_fields: 
        if field not in data or data[field] is None: 
            return jsonify({"error": f"Field '{field}' is required"}), 400
        
    new_user = User(
        email = data['email'],
        password = data['password']
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()),201

@app.route('/vehicle', methods=['POST'])
def create_vehicle():
    data = request.get_json()

    required_fields = ['name', 'model', 'price', 'manufacturer']
    for field in required_fields:
        if field not in data or data[field] is None:
            return jsonify({"error": f"Field '{field}' is required"}), 400

    new_vehicle = Vehicle(
        name=data['name'],
        model=data['model'],
        price=data['price'],
        manufacturer=data['manufacturer']
    )

    db.session.add(new_vehicle)
    db.session.commit()

    return jsonify(new_vehicle.serialize()), 201


@app.route('/people', methods=['POST'])
def create_people():
    data = request.get_json()

    required_fields = ['name', 'origin', 'eye_color', 'gender']
    for field in required_fields:
        if field not in data or data[field] is None:
            return jsonify({"error": f"Field '{field}' is required"}), 400

    new_people = People(
        name=data['name'],
        origin=data['origin'],
        eye_color=data['eye_color'],
        gender=data['gender']
    )

    db.session.add(new_people)
    db.session.commit()
    return jsonify(new_people.serialize()), 201


@app.route('/planet', methods=['POST'])
def create_planet():
    data = request.get_json()

    required_fields = ['name', 'climate', 'diameter', 'population']
    for field in required_fields:
        if field not in data or data[field] is None:
            return jsonify({"error": f"Field '{field}' is required"}), 400

    new_planet = Planet(
        name=data['name'],
        climate=data['climate'],
        diameter=data['diameter'],
        population=data['population']
    )

    db.session.add(new_planet)
    db.session.commit()

    return jsonify(new_planet.serialize()), 201

@app.route('/user/<int:user_id>/vehicle/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehicle(user_id, vehicle_id):
    
    user = User.query.get(user_id)
    if user is None: 
        return jsonify({"error": "user not found"}), 404

    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle is None: 
        return jsonify({"error": "vehicle not found"}), 404
    
    existing_favorite = Favorite.query.filter_by(user_id=user_id, vehicle_id=vehicle_id).first()
    if existing_favorite: 
        return jsonify({"error": "favorite already exists"}), 409 
    
    new_favorite = Favorite(user_id=user_id, vehicle_id=vehicle_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify(new_favorite.serialize()),201

@app.route('/user/<int:user_id>/people/<int:people_id>', methods=['POST'])
def add_favorite_people(user_id, people_id):

    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error":"user not found"}), 404 

    people = People.query.get(people_id)
    if people is None: 
        return jsonify({"error":"people not found"}), 404 

    existing_favorite = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
    if existing_favorite: 
        return jsonify({"error": "favorite already exists"}), 409 

    new_favorite = Favorite(user_id=user_id, people_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify(new_favorite.serialize()), 201 

@app.route('/user/<int:user_id>/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id): 

    user = User.query.get(user_id)
    if user is None: 
        return jsonify({"error": "user not found"}), 404 
    
    planet = Planet.query.get(planet_id)
    if planet is None: 
        return jsonify({"error": "planet not found"}), 404 

    existing_favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if existing_favorite: 
        return jsonify({"error": "favorite already exists"}), 409 
    
    new_favorite = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify(new_favorite.serialize()), 201

@app.route('/favorite/planet/<int:user_id>/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite is None: 
        return jsonify({"error": "favorite planet not found"}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": f"favorite planet {planet_id} deleted"}), 200

@app.route('/favorite/people/<int:user_id>/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(user_id, people_id):
    favorite = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
    if favorite is None: 
        return jsonify({"error": "favorite people not found"}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message" : f"favorite people {people_id} deleted"}), 200

@app.route('/favorite/vehicle/<int:user_id>/<int:vehicle_id>', methods=['DELETE'])
def delete_favorite_vehicle(user_id, vehicle_id):
    favorite = Favorite.query.filter_by(user_id=user_id, vehicle_id=vehicle_id).first()
    if favorite is None: 
        return jsonify({"error": "favorite vehicle not found"}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message" : f"favorite vehicle {vehicle_id} deleted"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
