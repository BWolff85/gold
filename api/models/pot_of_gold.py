from api.db import db
import sys
from sqlalchemy.exc import SQLAlchemyError
from api.models.pot_of_gold_history import pot_of_gold_history_model

class pot_of_gold_model(db.Model):
    __tablename__ = 'pot_of_gold'

    pot_of_gold_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    pot_of_gold_name = db.Column(db.String(255))
    current_amount = db.Column(db.Float(2))
    auto_increment = db.Column(db.Boolean)

    def __init__(self, user_id, pot_of_gold_name, current_amount, auto_increment, pot_of_gold_id=None):
        self.user_id = user_id
        self.pot_of_gold_name = pot_of_gold_name
        self.current_amount = current_amount
        self.auto_increment = auto_increment
        self.pot_of_gold_id = pot_of_gold_id
        print('from model, Pot id ' + str(self.pot_of_gold_id), file=sys.stderr)

    def json(self):
        return {
            "pot_of_gold_id": self.pot_of_gold_id,
            "user_id": self.user_id,
            "pot_of_gold_name": self.pot_of_gold_name,
            "current_amount": self.current_amount,
            "auto_increment": self.auto_increment
        }

    def is_loaded(self):
        return hasattr(self, 'pot_of_gold_id') and self.pot_of_gold_id > 0

    def save_to_db(self):
        print('Attmpting to save to db ' + str(self.json()), file=sys.stderr)
        try:
            if not self.pot_of_gold_id:
                db.session.add(self)
            else:
                db.session.merge(self)
            db.session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print('An error occurred ' + str(error), file=sys.stderr)

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_ai_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id, auto_increment=1)

    @classmethod
    def find_by_id(cls, pot_of_gold_id):
        return cls.query.filter_by(pot_of_gold_id=pot_of_gold_id).first()

    @classmethod
    def find_by_name(cls, user_id, pot_of_gold_name):
        return cls.query.filter_by(user_id=user_id, pot_of_gold_name=pot_of_gold_name).first()

    @classmethod
    def log_increment(cls, pot_of_gold_id, previous_amount, new_amount, comment):
        print('attempting to log auto increment ', file=sys.stderr)
        history = pot_of_gold_history_model(pot_of_gold_id=pot_of_gold_id, previous_amount=previous_amount, new_amount=new_amount, comment=comment)
        try:
            history.save_to_db()
        except:
            print('unable to log auto increment ', file=sys.stderr)
            return false
