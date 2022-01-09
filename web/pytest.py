# from api.AutoIncrement import AutoIncrement
# autoI = AutoIncrement()
# ret = autoI.auto_increment_user(1)
# print(ret)
# print('hello world')
from api.models.pot_of_gold import pot_of_gold

data = {'pot_of_gold_id': 1, 'user_id': 1, 'pot_of_gold_name': 'Stuff', 'current_amount': 118, 'auto_increment': 1}
id = 1
Pot = pot_of_gold()
Pot.load_by_id(id)
print(Pot.pot_of_gold_name)