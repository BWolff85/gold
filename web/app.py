from flask import Flask, render_template, request
from flask import jsonify
import requests
import sys

from werkzeug.utils import redirect


app = Flask(__name__)

@app.route('/dbtest')
def dbtest():
    print('You have reached the db test', file=sys.stderr)
    url = 'http://api:3000/dbtest'
    r = requests.get(url)
    print('Request has returned', file=sys.stderr)
    return "testing: " + str(r.json())

@app.route('/apitest')
def apitest():
    print('You have reached the api test', file=sys.stderr)
    url = 'http://api:3000'
    r = requests.get(url)
    print('Request has returned', file=sys.stderr)
    print(r, file=sys.stderr)
    # return "testing: " + str(r.json())
    return jsonify({"message": r.json()})

@app.route('/historytest')
def historytest():
    pot_id = 2
    print('you have reached the pot history test', file=sys.stderr)
    url = 'http://api:3000/pots_of_gold/history/' + str(pot_id)
    r = requests.get(url)
    print('Request has returned', file=sys.stderr)
    historylist = r.json()
    print(str(historylist), file=sys.stderr)
    return "testing: " + str(r.json())


@app.route('/pots/<user_id>')
@app.route('/pots', defaults={'user_id': 1})
def pots_of_gold(user_id):
    ai_url = 'http://api:3000/test_auto_increment/' + str(user_id)
    ai_r = requests.get(ai_url)
    if not ai_r:
        print("Failed to auto increment", file=sys.stderr)
    url = 'http://api:3000/pots_of_gold'
    r = requests.get(url)
    print('Request has returned', file=sys.stderr)
    potlist = r.json()
    print(str(potlist), file=sys.stderr)
    pots = potlist['pots']
    return render_template("pots_of_gold.html", pots=pots)

@app.route('/')
def hello_whale():
    return render_template("whale_hello.html")

@app.route('/new')
def new_pot():
    return render_template("new_pot_of_gold.html")

@app.route('/delete/<int:pot_of_gold_id>')
def delete_pot(pot_of_gold_id):
    url = 'http://api:3000/pot_of_gold/' + str(pot_of_gold_id)
    r = requests.delete(url)
    return redirect('/pots')

@app.route('/deposit',  methods=["POST"])
def deposit():
    pot_id = request.form.get('pot_of_gold_id')
    user_id = request.form.get('user_id')
    current = request.form.get('current_amount')
    pot_of_gold_name = request.form.get('pot_of_gold_name')
    auto_increment = request.form.get('auto_increment')
    amount = request.form.get('amount')
    current_amount = float(current) + float(amount)
    comment = request.form.get('comment')
    previous_amount = float(current)
    payload = {"user_id": user_id, "pot_of_gold_name": pot_of_gold_name, "auto_increment": auto_increment,
               "current_amount": current_amount,"pot_of_gold_id": pot_id, "comment": comment, "previous_amount": previous_amount}
    print('Pot id ' + str(pot_id) + " deposit", file=sys.stderr)
    url = 'http://api:3000/pot_of_gold'
    r = requests.post(url, data=payload)
    return redirect('/edit/' + pot_id)

@app.route('/debit',  methods=["POST"])
def debit():
    pot_id = request.form.get('pot_of_gold_id')
    user_id = request.form.get('user_id')
    current = request.form.get('current_amount')
    pot_of_gold_name = request.form.get('pot_of_gold_name')
    auto_increment = request.form.get('auto_increment')
    amount = request.form.get('amount')
    current_amount = float(current) - float(amount)
    previous_amount = float(current)
    comment = request.form.get('comment')
    payload = {"user_id": user_id, "pot_of_gold_name": pot_of_gold_name, "auto_increment": auto_increment,
               "current_amount": current_amount, "pot_of_gold_id": pot_id, "comment": comment, "previous_amount": previous_amount}
    print('Pot id ' + str(pot_id), file=sys.stderr)
    url = 'http://api:3000/pot_of_gold'
    r = requests.post(url, data=payload)
    return redirect('/edit/' + pot_id)

@app.route('/edit/<int:pot_of_gold_id>')
def edit_pot(pot_of_gold_id):
    print('You have reached the pots_of_gold test', file=sys.stderr)
    url = 'http://api:3000/pot_of_gold/' + str(pot_of_gold_id)
    r = requests.get(url)
    print('Request has returned', file=sys.stderr)
    pot = r.json()


    history_url = 'http://api:3000/pots_of_gold/history/' + str(pot_of_gold_id)
    history_r = requests.get(history_url)
    print('History Request has returned', file=sys.stderr)
    history_list = history_r.json()
    history = history_list['pot_history']
    # return render_template("pot_of_gold.html", pot=pot)

    increment_url = 'http://api:3000/pot_auto_increment/' + str(pot_of_gold_id)
    increment_r = requests.get(increment_url)
    print('Increment request has returned', file=sys.stderr)
    increment = increment_r.json()
    print(increment, file=sys.stderr)

    try:
        print('Working with pot ' + str(pot["pot_of_gold_id"]), file=sys.stderr)
        return render_template("pot_of_gold.html", pot=pot, history_list=history, increment=increment)
    except:
        return "SOMETHING HAS GONE WRONG " + str(pot)


@app.route('/update',  methods=["POST"])
def update():
    print('You have reached the pots_of_gold update', file=sys.stderr)

    pot_id = request.form.get('pot_of_gold_id')
    user_id = request.form.get('user_id')
    pot_of_gold_name = request.form.get('pot_of_gold_name')
    auto_increment = request.form.get('auto_increment')
    current_amount = request.form.get('current_amount')
    payload = {"user_id": user_id, "pot_of_gold_name": pot_of_gold_name, "auto_increment": auto_increment,
               "current_amount": current_amount, "pot_of_gold_id": pot_id}
    print('Pot id ' + str(pot_id), file=sys.stderr)
    print(payload, file=sys.stderr)
    url = 'http://api:3000/pot_of_gold'
    r = requests.post(url, data=payload)
    return redirect('/edit/' + str(pot_id))

@app.route('/increment_update',  methods=["POST"])
def increment_update():
    print('You have reached the increment update', file=sys.stderr)
    pot_of_gold_id = request.form.get('pot_of_gold_id')
    auto_increment_option_id = request.form.get('auto_increment_option_id')
    increment_amount = request.form.get('increment_amount')
    most_recent_increment = request.form.get('most_recent_increment')
    next_increment = request.form.get('next_increment')
    payload = {"pot_of_gold_id": pot_of_gold_id, "auto_increment_option_id": auto_increment_option_id, "increment_amount": increment_amount,
               "most_recent_increment": most_recent_increment, "next_increment": next_increment}
    print('pot_of_gold_id ' + str(pot_of_gold_id), file=sys.stderr)
    print(payload, file=sys.stderr)
    url = 'http://api:3000/pot_auto_increment'
    r = requests.post(url, data=payload)
    return redirect('/edit/' + str(pot_of_gold_id))

@app.route('/create', methods=['POST'])
def create_pot():
    uid = request.form['user_id']
    name = request.form['pot_name']
    auto_option = request.form['auto_increment']
    auto = 1 if int(auto_option) > 0 else 0
    auto_date = request.form['first_increment_date']
    amt = request.form['increment_amount']
    init_val = request.form['current_amount']
    payload = {"user_id": uid, "pot_of_gold_name": name, "auto_increment": auto, "current_amount": init_val,
               "increment_amount": amt, "next_increment": auto_date}
    print('You want to create a new pot ' + str(payload), file=sys.stderr)
    url = 'http://api:3000/pot_of_gold'
    r = requests.post(url, data=payload)
    return redirect('/pots')

@app.route('/pots/<int:pot_id>/project/', methods=['GET', 'POST'])
@app.route('/pots/<int:pot_id>/project/<string:target_date>/', methods=['GET', 'POST'])
def project(pot_id, target_date = None):
    if request.method == "POST":
        target_date = request.form["target_date"]
    api_url = f"http://api:3000/pots/{pot_id}/project/{target_date}"
    response = requests.get(api_url)
    data = response.json()
    return render_template("project.html", pot_id=pot_id, target_date=target_date, data=data)

@app.route('/test_auto_increment', defaults={'user_id': 1})
@app.route('/test_auto_increment/<user_id>')
def test_auto_increment(user_id):
    print('You have reached the test_auto_increment test', file=sys.stderr)
    print('User ID is ' + str(user_id), file=sys.stderr)
    url = 'http://api:3000/test_auto_increment/' + str(user_id)
    r = requests.get(url)
    print('Request has returned', file=sys.stderr)
    pot = r.json()
    return "testing: " + str(pot)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)