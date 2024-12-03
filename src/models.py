from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#class User(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    #email = db.Column(db.String(120), unique=True, nullable=False)
    #password = db.Column(db.String(80), unique=False, nullable=False)
    #is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    #def __repr__(self):
        #return '<User %r>' % self.username

    #def serialize(self):
        #return {
            #"id": self.id,
            #"email": self.email,
            # do not serialize the password, its a security breach
        #}
    

class User(db.Model):
    __tablename__ = 'users'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    first_name = db.Column(db.String, unique=False, nullable=False)
    last_name = db.Column(db.String, unique=False, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String, unique=False, nullable=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id":self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone_number": self.phone_number,
            }
    

class Planet(db.Model):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String, unique=False, nullable=False)
    population = db.Column(db.String, unique=False, nullable=False)
    climate = db.Column(db.String, unique=False, nullable=False)
    #films = db.Column(db.String, unique=False, nullable=False)
    #user_id = db.Column(db.Integer, ForeignKey('users.id'))
    #user = relationship(User)

    def to_dict(self):
        return {}
    
    def serialize(self):
        return {
            "id":self.id,
            "planet_name": self.planet_name,
            "population": self.population,
            "climate": self.climate,
            }
    
class Character(db.Model):
    __tablename__ = 'characters'

    id = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.String, unique=False, nullable=False)
    birth_year = db.Column(db.String, unique=False, nullable=False)
    gender = db.Column(db.String, unique=False, nullable=False)
    #homeworld = db.Column(db.String, unique=False, nullable=False)
    #films = db.Column(db.String, unique=False, nullable=False)
    #user_id = db.Column(db.Integer, ForeignKey('users.id'))
    #user = relationship(User)

    def to_dict(self):
        return {}  
    def serialize(self):
        return {
            "id":self.id,
            "character_name": self.character_name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            }

class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    vehicle_name = db.Column(db.String, unique=False, nullable=False)
    model = db.Column(db.String, unique=False, nullable=False)
    #length = db.Column(db.String, unique=False, nullable=False)
    #crew = db.Column(db.String, unique=False, nullable=False)
    #films = db.Column(db.String, unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship(User)

    def to_dict(self):
        return {}  
    def serialize(self):
        return {
            "id":self.id,
            "name": self.name,
            "model": self.model,
            } 
    
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)  

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship(User)

    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=True)
    character = db.relationship(Character)

    #planet_id = db.Column(db.Integer, db.ForeignKey('Planet.id'), nullable=True)
    #planet = db.relationship(Planet)

    #vehicle_id = db.Column(db.Integer, db.ForeignKey('Vehicle.id'), nullable=True)
    #vehicle = db.relationship(Vehicle)

    def serialize(self):
        return {
            "id": self.user_id,
            "character_id": self.character_id,
            #"planet_id": self.planet_id,
            #"vehicle_id": self.vehicle_id,
        }