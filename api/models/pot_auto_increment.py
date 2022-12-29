from api.db import db
import sys

class pot_auto_increment_model(db.Model):
    __tablename__ = 'pot_auto_increment'

    pot_of_gold_id = db.Column(db.Integer, primary_key=True)
    auto_increment_option_id = db.Column(db.Integer)
    increment_amount = db.Column(db.Float(2))
    most_recent_increment = db.Column(db.TIMESTAMP())
    next_increment = db.Column(db.TIMESTAMP())

    def __init__(self, pot_of_gold_id, auto_increment_option_id, increment_amount, most_recent_increment, next_increment):
        self.pot_of_gold_id = pot_of_gold_id
        self.auto_increment_option_id = auto_increment_option_id
        self.increment_amount = increment_amount
        self.most_recent_increment = most_recent_increment
        self.next_increment = next_increment

    def json(self):
        return {
            "pot_of_gold_id": self.pot_of_gold_id,
            "auto_increment_option_id": self.auto_increment_option_id,
            "increment_amount": self.increment_amount,
            "most_recent_increment": (self.most_recent_increment.strftime("%Y-%m-%d") if self.most_recent_increment else ""),
            "next_increment": (self.next_increment.strftime("%Y-%m-%d") if self.next_increment else "")
        }


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
    def find_by_id(cls, pot_of_gold_id):
        return cls.query.filter_by(pot_of_gold_id=pot_of_gold_id).first()

