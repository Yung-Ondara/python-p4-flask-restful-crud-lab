#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Plants(Resource):

    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        data = request.get_json()

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)


api.add_resource(Plants, '/plants')


class PlantByID(Resource):

    def get(self, id):
        plant = Plant.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(plant), 200)


api.add_resource(PlantByID, '/plants/<int:id>')

app.patch('/plants/:id', async (req, res) => {
  const { id } = req.params;
  const updates = req.body;

  try {
    const plant = await Plant.findByPk(id); // or use findById if using Mongoose

    if (!plant) {
      return res.status(404).json({ error: 'Plant not found' });
    }

    await plant.update(updates); // Sequelize syntax
    res.json(plant);
  } catch (error) {
    res.status(500).json({ error: 'Server error' });
  }
});

app.delete('/plants/:id', async (req, res) => {
  const { id } = req.params;

  try {
    const plant = await Plant.findByPk(id);

    if (!plant) {
      return res.status(404).json({ error: 'Plant not found' });
    }

    await plant.destroy(); // Sequelize syntax
    res.status(204).send(); // 204 No Content
  } catch (error) {
    res.status(500).json({ error: 'Server error' });
  }
});

if __name__ == '__main__':
    app.run(port=5555, debug=True)
