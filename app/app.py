#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound
from flask_cors import CORS

from models import db, Hero , Power , HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

ma = Marshmallow(app)

class HeroSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Hero
        load_instance = True

hero_schema = HeroSchema()
heroes_schema = HeroSchema(many=True)

class PowerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Power

power_schema = PowerSchema()
powers_schema = PowerSchema(many=True)

class HeroPowerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HeroPower

hero_power_schema = HeroPowerSchema()

api = Api(app)

class Index(Resource):

    def get(self):

        response_dict = {
            "index": "Welcome to the Superheroes RESTful API",
        }

        response = make_response(
            jsonify(response_dict),
            200,
        )
        response.headers["Content-Type"] = "application/json"

        return response

class Heroes(Resource):

    def get(self):

        heroes = Hero.query.all()

        if heroes :
            response_data = []
            for hero in heroes :
                response_data.append({
                    "id":hero.id,
                    "name":hero.name,
                    "super_name":hero.super_name
                })

            response = make_response(
                jsonify(response_data),
                200,
            )
            response.headers["Content-Type"] = "application/json"

            return response
        
        else :
            response = make_response(
                jsonify({"error":" Heroes are not currently in database"}),
                  404
                )
            response.headers["Content-Type"] = "application/json"

            return response

    def post(self):

        new_hero = Hero(
            name=request.json['name'],
            super_name=request.json['super_name'],
        )
        
        try: 
            db.session.add(new_hero)
            db.session.commit()

            response = make_response(
                hero_schema.dump(new_hero),
                201,
            )
            response.headers["Content-Type"] = "application/json"

            return response
        
        except Exception as e:
            db.session.rollback()  

            response = make_response(
                jsonify({"errors": ["validation errors"]}),
                400  
            )
            response.headers["Content-Type"] = "application/json"

            return response

class HeroByID(Resource):

    def get(self, id):

        hero = Hero.query.filter_by(id=id).first()

        if hero :
            hero_powers = HeroPower.query.filter_by(hero_id=id).all()
            powers_data = []

            for hp in hero_powers:
                power = db.session.get(Power, hp.power_id)
                if power:
                    powers_data.append({
                        "id": power.id,
                        "name": power.name,
                        "description": power.description
                    })

            response_data = {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
                "powers": powers_data
            }

            response = make_response(
                jsonify(response_data),
                200,
            )
            response.headers["Content-Type"] = "application/json"

            return response
        
        else :
            response = make_response(
                jsonify({"error":" Hero not found"}),
                  404
                )
            response.headers["Content-Type"] = "application/json"

            return response

    def patch(self, id):

        hero = Hero.query.filter_by(id=id).first()

        if hero :
            for attr in request.form:
                setattr(hero, attr, request.json[attr])

            try:
                db.session.add(hero)
                db.session.commit()

                response = make_response(
                    hero_schema.dump(hero),
                    200
                )
                response.headers["Content-Type"] = "application/json"

                return response

            except Exception as e:
                db.session.rollback()  

                response = make_response(
                    jsonify({"errors": ["validation errors"]}),
                    400  
                )
                response.headers["Content-Type"] = "application/json"

                return response
            
        else :
            response = make_response(
                jsonify({"error": "Hero not found"}),
                404
            )
            response.headers["Content-Type"] = "application/json"

            return response
        
    def delete(self, id):

        hero = Hero.query.filter_by(id=id).first()

        if hero :
            db.session.delete(hero)
            db.session.commit()

            response_dict = {"message": "Hero successfully deleted"}

            response = make_response(
                jsonify(response_dict),
                200
            )
            response.headers["Content-Type"] = "application/json"

            return response
        else :
            response = make_response(
                jsonify({"error": "Hero not found"}),
                404
                )
            response.headers["Content-Type"] = "application/json"

            return response

class Powers(Resource):

    def get(self):

        powers = Power.query.all()

        if powers :
            response_data = []

            for power in powers :
                response_data.append({
                    "id":power.id,
                    "name":power.name,
                    "description":power.description,
                })

            response = make_response(
                jsonify(response_data),
                200,
            )
            response.headers["Content-Type"] = "application/json"

            return response
        
        else :
            response = make_response(
                jsonify({"error":" Powers are not currently in database"}),
                  404
                )
            response.headers["Content-Type"] = "application/json"

            return response

    def post(self):

        new_power = Power(
            name=request.json['name'],
            description=request.json['description'],
        )
        
        try : 
            db.session.add(new_power)
            db.session.commit()

            response = make_response(
                power_schema.dump(new_power),
                201,
            )
            response.headers["Content-Type"] = "application/json"

            return response
        
        except Exception as e:
            db.session.rollback()  

            response = make_response(
                jsonify({"errors": ["validation errors"]}),
                400  
            )
            response.headers["Content-Type"] = "application/json"

            return response

class PowerByID(Resource):

    def get(self, id):

        power = Power.query.filter_by(id=id).first()

        if power :

            response_data = {
                "id": power.id,
                "name": power.name,
                "description": power.description,
            }

            response = make_response(
                jsonify(response_data),
                200,
            )
            response.headers["Content-Type"] = "application/json"

            return response
        
        else :
            response = make_response(
                jsonify({"error":" Power not found"}),
                  404
                )
            response.headers["Content-Type"] = "application/json"

            return response

    def patch(self, id):

        power = Power.query.filter_by(id=id).first()

        if power :
            for attr in request.form:
                setattr(power, attr, request.json[attr])

            try:
                db.session.add(power)
                db.session.commit()

                response = make_response(
                    jsonify({"description" : "Updated description."}),
                    200
                )
                response.headers["Content-Type"] = "application/json"

                return response

            except Exception as e:
                db.session.rollback()  

                response = make_response(
                    jsonify({"errors": ["validation errors"]}),
                    400  
                )
                response.headers["Content-Type"] = "application/json"

                return response
            
        else :
            response = make_response(
                jsonify({"error": "Power not found"}),
                404
            )
            response.headers["Content-Type"] = "application/json"

            return response

    def delete(self, id):

        power = Power.query.filter_by(id=id).first()

        if power :
            db.session.delete(power)
            db.session.commit()

            response_dict = {"message": "Power successfully deleted"}

            response = make_response(
                jsonify(response_dict),
                200
            )
            response.headers["Content-Type"] = "application/json"

            return response
        else :
            response = make_response(
                jsonify({"error": "Power not found"}),
                404
                )
            response.headers["Content-Type"] = "application/json"

            return response

class HeroPowers(Resource):

    def post(self):

        hero = Hero.query.filter_by(id=request.json['hero_id']).first()
        power = Power.query.filter_by(id=request.json['power_id']).first()

        if hero and power :

            new_hero_power = HeroPower(
                strength=request.json['strength'],
                power_id=request.json['power_id'],
                hero_id=request.json['hero_id'],
            )
             
            try:
                db.session.add(new_hero_power)
                db.session.commit()

                hero_powers = HeroPower.query.filter_by(hero_id=request.json['hero_id']).all()
                powers_data = []

                for hp in hero_powers:
                    power = db.session.get(Power, hp.power_id)
                    if power:
                        powers_data.append({
                            "id": power.id,
                            "name": power.name,
                            "description": power.description
                        })

                response_data = {
                    "id": hero.id,
                    "name": hero.name,
                    "super_name": hero.super_name,
                    "powers": powers_data
                }

                response = make_response(
                    jsonify(response_data),
                    200,
                )
                response.headers["Content-Type"] = "application/json"

                return response
            
            except Exception as e:
                db.session.rollback()  

                response = make_response(
                    jsonify({"errors": ["validation errors"]}),
                    400  
                )
                response.headers["Content-Type"] = "application/json"

                return response
        
        else :
            response = make_response(
                  jsonify({"errors": ["Hero or Power id does not exist"]}),
                  400
            )
            response.headers["Content-Type"] = "application/json"

            return response

api.add_resource(Index, '/')
api.add_resource(Heroes, '/heroes')
api.add_resource(HeroByID, '/heroes/<int:id>')
api.add_resource(Powers, '/powers')
api.add_resource(PowerByID, '/powers/<int:id>')
api.add_resource(HeroPowers, '/hero_powers')

@app.errorhandler(NotFound)
def handle_not_found(e):

    response = make_response(
        jsonify({"Not Found": "The requested resource does not exist."}),
        404
    )
    response.headers["Content-Type"] = "application/json"

    return response

if __name__ == '__main__':
    app.run(port=5555)
