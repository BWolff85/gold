from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from flask import jsonify
from flask_restful import Api
from flask import current_app

import mysql.connector
from mysql.connector import Error
from werkzeug.utils import redirect
from api.AutoIncrement import AutoIncrement
from api.Projection import Projection
from api.resources.pot_of_gold import pot_of_gold_resource, pot_of_gold_list_resource
from api.resources.pot_of_gold_history import pot_of_gold_history_resource, pot_of_gold_history_list_resource
from api.resources.pot_auto_increment import pot_auto_increment_resource
from api.db import db
from datetime import datetime
import sys

app = Flask(__name__)
app.config.from_object("config.Config")
api = Api(app)

api.add_resource(pot_of_gold_resource, '/pot_of_gold/<int:pot_of_gold_id>', '/pot_of_gold')
api.add_resource(pot_of_gold_list_resource, '/pots_of_gold')


api.add_resource(pot_of_gold_history_resource, '/pot_of_gold_history/<int:pot_of_gold_history_id>', '/pot_of_gold_history')
api.add_resource(pot_of_gold_history_list_resource, '/pots_of_gold/history/<int:pot_of_gold_id>')

api.add_resource(pot_auto_increment_resource, '/pot_auto_increment/<int:pot_of_gold_id>', '/pot_auto_increment')

@app.route('/')
def hello_world():
    print("Brittany!!!!", file=sys.stderr)
    print(app.config['DB_NAME'], file=sys.stderr)
    print(current_app.config['SQLALCHEMY_DATABASE_URI'], file=sys.stderr)
    print('You have reached the api!', file=sys.stderr)
    return jsonify({"message": "Hello world!"})


@app.route('/test_auto_increment', defaults={'user_id': 1})
@app.route('/test_auto_increment/<user_id>')
def test_auto_increment(user_id):
    autoI = AutoIncrement()
    res = autoI.auto_increment_user(user_id)
    print('You have reached the api test_auto_increment test', file=sys.stderr)
    return jsonify({"msg": "BOO"})
    # return 'For %s, the last increment date was %s. It has increment option %s' % (user_id, test_date, option_id)

@app.route('/pots/<pot_id>/project/<target_date>')
def project_pot(pot_id, target_date):
    target = datetime.strptime(target_date, "%Y-%m-%d")
    projector = Projection()
    projections = projector.poject_pot(pot_id, target)
    return jsonify(projections)


@app.route('/dbtest')
def db_test():
    print('I hate this', file=sys.stderr)
    return jsonify({"message": "grrrrr"})

@app.route('/pot_history/<int:pot_of_gold_id>')
def pot_history(pot_of_gold_id):
    return jsonify({"message": "grrrrr"})

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True, host='0.0.0.0', port=3000)