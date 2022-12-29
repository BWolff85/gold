import sys
from flask_restful import Resource
from flask_restful import Resource, reqparse
from flask_restful import inputs
from flask import Flask, request
from api.models.pot_of_gold import pot_of_gold_model
from api.models.pot_of_gold_history import pot_of_gold_history_model

class pot_of_gold_resource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('pot_of_gold_id', type=int, location='form')
    parser.add_argument('user_id',  type=int, required=True, help="This field cannot be left blank!", location='form' )
    parser.add_argument('pot_of_gold_name', type=str, required=True, help="This field cannot be left blank!", location='form' )
    parser.add_argument('current_amount', type=float, location='form' )
    parser.add_argument('auto_increment', type=inputs.boolean, location='form' )

    def get(self, pot_of_gold_id):
        print('You have reached the pot_of_gold get resource', file=sys.stderr)
        pot_of_gold = pot_of_gold_model.find_by_id(pot_of_gold_id)
        if pot_of_gold:
            return pot_of_gold.json()
        return {"message": "pot of gold not found"}

    def post(self):
        print('You have reached the pot_of_gold post resource', file=sys.stderr)
        print(request.data, file=sys.stderr)
        data = pot_of_gold_resource.parser.parse_args()
        pot = pot_of_gold_model(**data)
        prev_amt = request.form.get("previous_amount", None)
        if (prev_amt is not None):
            comment = request.form["comment"]
            pot_of_gold_model.log_increment(pot_of_gold_id=pot.pot_of_gold_id, previous_amount=prev_amt, new_amount=pot.current_amount, comment=comment)

        try:
            pot.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500
        return pot.json(), 201

    def delete(self, pot_of_gold_id):
        pot = pot_of_gold_model.find_by_id(pot_of_gold_id)
        if pot:
            pot.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404

class pot_of_gold_list_resource(Resource):
    def get(self):
        print('You have reached the pot_of_gold_list_resource get resource', file=sys.stderr)
        return {"pots": [pot_of_gold.json() for pot_of_gold in pot_of_gold_model.query.all()]}



