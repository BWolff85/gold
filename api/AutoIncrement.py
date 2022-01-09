from math import floor

from api.models.pot_of_gold import pot_of_gold_model
from api.models.pot_auto_increment import pot_auto_increment_model
from api.models.auto_increment_options import auto_increment_options_model
from api.models.pot_of_gold_history import pot_of_gold_history_model
from datetime import date
import datetime
import sys

class AutoIncrement:

    def __init__(self):
        self.thingy = "hmph"

    def auto_increment_user(self, uid):
        pots = pot_of_gold_model.find_ai_by_user_id(uid)
        if pots:
            for pot in pots:
                ai = pot_auto_increment_model.find_by_id(pot.pot_of_gold_id)
                if not pot.auto_increment or not ai:
                    print("Pot " + str(pot.pot_of_gold_id) + " should not auto increment")
                    continue
                print('pot ' + str(pot.pot_of_gold_id), file=sys.stderr)

                option = auto_increment_options_model.find_by_id(ai.auto_increment_option_id)
                print('pot ' + str(pot.pot_of_gold_id) + ' has an increment type of ' + option.auto_increment_option, file=sys.stderr)
                option = auto_increment_options_model.find_by_id(ai.auto_increment_option_id)
                self.bi_weekly(pot, ai)
        return "BOO"

    def bi_weekly(self, pot: pot_of_gold_model, auto_inc: pot_auto_increment_model):
        today = date.today()
        if auto_inc.most_recent_increment:
            targetDate = auto_inc.most_recent_increment.date()
            print('most_recent_increment ' +targetDate.strftime("%m/%d/%Y, %H:%M:%S"), file=sys.stderr)
        else:
            d = datetime.timedelta(days=14)
            targetDate = auto_inc.next_increment.date() - d

        datediff = today - targetDate
        print('pot ' + str(pot.pot_of_gold_id) + ' date diff from ' + today.strftime("%m/%d/%Y, %H:%M:%S") + ' to ' + targetDate.strftime("%m/%d/%Y, %H:%M:%S") + ' in days is ' + str(datediff.days), file=sys.stderr)
        incs = floor(datediff.days / 14)
        print('pot ' + str(pot.pot_of_gold_id) + ' should be incremented ' + str(incs) + ' times', file=sys.stderr)
        if incs > 0:
            original_amount = pot.current_amount
            new_current_amount = pot.current_amount + (auto_inc.increment_amount * incs)
            mrd = 14 * incs
            incdays = datetime.timedelta(days=mrd)
            print('test ' + str(incdays) + ' and ', file=sys.stderr)
            new_most_recent_increment = targetDate + incdays
            new_next = new_most_recent_increment + datetime.timedelta(days=14)
            print("new amount is " + str(new_current_amount) + " new most recent is " + new_most_recent_increment.strftime("%m/%d/%Y, %H:%M:%S") + " and new next is " + new_next.strftime("%m/%d/%Y, %H:%M:%S"), file=sys.stderr)
            pot.current_amount = new_current_amount
            auto_inc.most_recent_increment = new_most_recent_increment
            auto_inc.next_increment = new_next
            pot.save_to_db()
            auto_inc.save_to_db()
            pot_of_gold_model.log_increment(pot_of_gold_id=pot.pot_of_gold_id, previous_amount=original_amount, new_amount=pot.current_amount, comment="Auto Increment")

    # @classmethod
    # def log_increment(cls, pot_of_gold_id, previous_amount, current_amount):
    #     print('attempting to log auto increment ', file=sys.stderr)
    #     history = pot_of_gold_history_model(pot_of_gold_id=pot_of_gold_id, previous_amount=previous_amount, new_amount=current_amount, comment="Auto Increment")
    #     try:
    #         history.save_to_db()
    #     except:
    #         print('unable to log auto increment ', file=sys.stderr)
    #         return false

    def auto_increment_pot(self, pot: pot_of_gold_model):
        if not pot.auto_increment:
            return
