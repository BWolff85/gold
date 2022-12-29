import sys
from datetime import datetime
from flask_restful import Resource
from flask_restful import Resource, reqparse
from flask_restful import inputs
from flask import Flask, request
from api.models.pot_auto_increment import pot_auto_increment_model

class pot_auto_increment_resource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('pot_of_gold_id', type=int, location='form')
    parser.add_argument('auto_increment_option_id',  type=int, required=True, default=1, help="This field cannot be left blank!", location='form' )
    parser.add_argument('increment_amount', type=float, required=True, default=0.0, help="This field cannot be left blank!", location='form' )
    parser.add_argument('most_recent_increment', type=inputs.date, location='form' )
    parser.add_argument('next_increment', type=inputs.date, location='form' )

    def get(self, pot_of_gold_id):
      print('You have reached the pot_auto_increment get resource', file=sys.stderr)
      pot_auto_increment = pot_auto_increment_model.find_by_id(pot_of_gold_id)
      if pot_auto_increment:
          return pot_auto_increment.json()

    def post(self):
      print('You have reached the pot_auto_increment post resource', file=sys.stderr)
      data = pot_auto_increment_resource.parser.parse_args()
      inc = pot_auto_increment_model(**data)

      try:
          inc.save_to_db()
      except:
          return {"message": "An error occurred inserting the item."}, 500
      return inc.json(), 201