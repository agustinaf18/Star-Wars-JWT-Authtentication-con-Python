from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), unique=False, nullable=False)
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username

#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             # do not serialize the password, its a security breach
#         }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # user_name = db.Column(db.String(250) , nullable=False)
    password = db.Column(db.String(250) , nullable=False)
    favorite = db.relationship('Favourite', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # "user_name": self.user_name,
            # do not serialize the password, its a security breach
        }

# class Person(db.Model):
#     # Here we define columns for the table person
#     # Notice that each column is also a normal Python instance attribute.
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(250), nullable=False)

#     def __repr__(self):
#         return '<Person %r>' % self.id

#     def serialize(self):
#         return {
#             "id": self.id,
#             "name": self.name,
#             # do not serialize the password, its a security breach
#         }



#esta clase nos permite trar todos los characters de starwars
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))
    gender = db.Column(db.String(250))
    hair_color = db.Column(db.String(250))
    height = db.Column(db.Integer)
    skin_color = db.Column(db.String(250))
    favorite = db.relationship('Favourite', backref='character', lazy=True)

    def __repr__(self):
        return '<Character %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "character_name": self.character_name,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "height": self.height,
            "skin_color": self.skin_color,
        }

#esta clase nos permite trar todos los planets de starwars
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String(250))
    climate = db.Column(db.String(250))
    population = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    diameter = db.Column(db.Integer)
    favorite = db.relationship('Favourite', backref='planet', lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "planet_name": self.planet_name,
            "climate": self.climate,
            "population": self.population,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period,
            "diameter": self.diameter,
        }     


class Vehicle(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    vehicle_name = db.Column(db.String(250))
    cargo_capacity = db.Column(db.Integer)
    consumables = db.Column(db.String(250))
    cost_in_credits = db.Column(db.Integer)
    crew_capacity = db.Column(db.Integer)
    manufacturer = db.Column(db.String(250))
    favorite = db.relationship('Favourite', backref='vehicle', lazy=True)

    def __repr__(self):
        return '<Vehicle %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "vehicle_name": self.vehicle_name,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "cost_in_credits": self.cost_in_credits,
            "crew_capacity": self.crew_capacity,
            "manufacturer": self.manufacturer,
        }   


class Favourite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"))
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicle.id"))

    def __repr__(self):
        return '<Favourite %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id,
            "vehicle_id": self.vehicle_id,
        }  

    