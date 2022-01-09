import sys
import datetime
from flask_restful import Resource
from flask_restful import Resource, reqparse
from flask import Flask, request
from api.models.pot_of_gold_history import pot_of_gold_history_model

class pot_of_gold_history_resource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('pot_of_pot_of_gold_history_idgold_id', type=int)
    parser.add_argument('pot_of_gold_id', type=int)
    parser.add_argument('previous_amount',  type=float, required=True, help="This field cannot be left blank!" )
    parser.add_argument('new_amount', type=float, required=True, help="This field cannot be left blank!" )
    parser.add_argument('comment', type=str )
    parser.add_argument('pot_of_gold_history_timestamp', type=lambda x: datetime.strptime(x,'%Y-%m-%dT%H:%M:%S') )

    def get(self, pot_of_gold_history_id):
        print('You have reached the pot_of_gold_history get resource', file=sys.stderr)
        pot_of_gold_history = pot_of_gold_history_model.find_by_id(pot_of_gold_history_id)
        if pot_of_gold_history:
            return pot_of_gold_history.json()
        return {"message": "pot of gold history not found"}

    def post(self):
        print('You have reached the pot_of_gold_history post resource', file=sys.stderr)
        data = pot_of_gold_history_resource.parser.parse_args()
        pot_history = pot_of_gold_history_model(**data)
        try:
            pot_history.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500
        return pot_history.json(), 201

    def delete(self, pot_of_gold_history_id):
        pot_history = pot_of_gold_history_model.find_by_id(pot_of_gold_history_id)
        if pot_history:
            pot_history.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404

class pot_of_gold_history_list_resource(Resource):
    def get(self, pot_of_gold_id):
        print('You have reached the pot_of_gold_history_list_resource get resource', file=sys.stderr)
        return {"pot_history": [pot_of_gold_history.json() for pot_of_gold_history in pot_of_gold_history_model.query.filter_by(pot_of_gold_id=pot_of_gold_id).order_by(pot_of_gold_history_model.pot_of_gold_history_timestamp.desc())]}



