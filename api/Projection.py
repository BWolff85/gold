from math import floor

from api.models.pot_of_gold import pot_of_gold_model
from api.models.pot_auto_increment import pot_auto_increment_model
from api.models.auto_increment_options import auto_increment_options_model
from api.models.pot_of_gold_history import pot_of_gold_history_model
from datetime import date
import datetime
import sys

class Projection:

    def __init__(self):
        self.thingy = "hmph"

    def poject_pot(self, pot_id, target_date):
        pot = pot_of_gold_model.find_by_id(pot_id)
        ai = pot_auto_increment_model.find_by_id(pot.pot_of_gold_id)
        if not pot.auto_increment or not ai:
            print("Pot " + str(pot.pot_of_gold_id) + " does not auto increment")
            return
        print('pot ' + str(pot.pot_of_gold_id), file=sys.stderr)

        option = auto_increment_options_model.find_by_id(ai.auto_increment_option_id)
        print('pot ' + str(pot.pot_of_gold_id) + ' has an increment type of ' + option.auto_increment_option, file=sys.stderr)
        projections = self.bi_weekly(target_date, pot, ai)
        return projections

    def bi_weekly(self, target_date, pot: pot_of_gold_model, auto_inc: pot_auto_increment_model):
        start_date = self.get_start_date(auto_inc)
        increment_days = datetime.timedelta(days=14)
        start_amount = pot.current_amount

        projections = []
        while start_date <= target_date.date():
            start_amount += auto_inc.increment_amount

            projection = {
                "increment_date": start_date.strftime("%m/%d/%Y"),
                "total_amount": start_amount
            }
            projections.append(projection)
            start_date += increment_days
        return projections

    def get_start_date(self, auto_inc: pot_auto_increment_model):
        if auto_inc.most_recent_increment:
            d = datetime.timedelta(days=14)
            start_date = auto_inc.most_recent_increment.date() + d
        else:
            start_date = auto_inc.next_increment.date()
        return start_date
