#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS  # Added CORS to handle cross-origin requests

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

# Enable CORS
CORS(app)

# Initialize Flask extensions
migrate = Migrate(app, db)
db.init_app(app)

# Initialize Flask-RESTful API
api = Api(app)

# Plants Resource (handles GET all plants and POST new plant)
class Plants(Resource):
    def get(self):
        # Retrieve all plants and serialize them to a list of dictionaries
        response_dict_list = [plant.to_dict() for plant in Plant.query.all()]
        response = make_response(response_dict_list, 200)
        return response

    def post(self):
        try:
            data = request.get_json()
            # Create a new plant instance
            new_plant = Plant(name=data['name'], image=data['image'], price=data['price'])
            db.session.add(new_plant)
            db.session.commit()

            # Serialize the new plant to a dictionary and return it in the response
            response_dict = new_plant.to_dict()
            response = make_response(response_dict, 201)
            return response
        except Exception as e:
            # Rollback the session in case of any database error
            db.session.rollback()
            return make_response({'error': str(e)}, 400)

# PlantByID Resource (handles GET plant by id)
class PlantByID(Resource):
    def get(self, id):
        # Retrieve plant by ID
        plant = Plant.query.get(id)
        if not plant:
            return make_response({'error': 'Plant not found'}, 404)

        # Serialize the plant to a dictionary and return it in the response
        response_dict = plant.to_dict()
        return make_response(response_dict, 200)

# Add the resources to the API
api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

# Run the Flask application
if __name__ == '__main__':
    app.run(port=5555, debug=True)
