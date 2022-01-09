from api.db import db
import sys
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func

class pot_of_gold_history_model(db.Model):
    __tablename__ = 'pot_of_gold_history'

    pot_of_gold_history_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pot_of_gold_id = db.Column(db.Integer, primary_key=True)
    previous_amount = db.Column(db.Float(2))
    new_amount = db.Column(db.Float(2))
    comment = db.Column(db.String(255))
    pot_of_gold_history_timestamp = db.Column(db.TIMESTAMP(), server_default=func.now())

    def __init__(self, pot_of_gold_id, previous_amount, new_amount, comment, pot_of_gold_history_timestamp=None, pot_of_gold_history_id=None):
        self.pot_of_gold_id = pot_of_gold_id
        self.previous_amount = previous_amount
        self.new_amount = new_amount
        self.comment = comment
        self.pot_of_gold_history_timestamp = pot_of_gold_history_timestamp
        self.pot_of_gold_history_id = pot_of_gold_history_id
        print('from history model, Pot history id ' + str(self.pot_of_gold_history_id), file=sys.stderr)

    def json(self):
        timestamp = (self.pot_of_gold_history_timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.pot_of_gold_history_timestamp else '')
        return {
            "pot_of_gold_history_id": self.pot_of_gold_history_id,
            "pot_of_gold_id": self.pot_of_gold_id,
            "previous_amount": self.previous_amount,
            "new_amount": self.new_amount,
            "comment": self.comment,
            "pot_of_gold_history_timestamp": timestamp
        }

    def is_loaded(self):
        return hasattr(self, 'pot_of_gold_history_id') and self.pot_of_gold_history_id > 0

    def save_to_db(self):
        print('Attmpting to save to db ' + str(self.json()), file=sys.stderr)
        try:
            if not self.pot_of_gold_history_id:
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
    def find_pot_history(cls, pot_of_gold_id):
        return cls.query.filter_by(pot_of_gold_id=pot_of_gold_id)

    @classmethod
    def find_by_id(cls, pot_of_gold_history_id):
        return cls.query.filter_by(pot_of_gold_history_id=pot_of_gold_history_id).first()

    @classmethod
    def find_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id)
