from api.db import db
import sys

class auto_increment_options_model(db.Model):
    __tablename__ = 'auto_increment_options'

    auto_increment_option_id = db.Column(db.Integer, primary_key=True)
    auto_increment_option = db.Column(db.String(255))

    def __init__(self, auto_increment_option_id, auto_increment_option):
        self.auto_increment_option_id = auto_increment_option_id
        self.auto_increment_option = auto_increment_option

    def json(self):
        return {
            "auto_increment_option_id": self.auto_increment_option_id,
            "auto_increment_option": self.auto_increment_option
        }

    def save_to_db(self):
        print('Attmpting to save to db ' + str(self), file=sys.stderr)
        db.session.add(self)
        db.session.commit()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, auto_increment_option_id):
        return cls.query.filter_by(auto_increment_option_id=auto_increment_option_id).first()

    @classmethod
    def find_by_name(cls, auto_increment_option):
        return cls.query.filter_by(auto_increment_option=auto_increment_option).first()
