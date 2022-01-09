from os import path
import datetime


class Logger:
    filename = "/app/api/logs/pots_of_gold_log.log"

    @staticmethod
    def log(pot_id, message):
        try:
            time = datetime.datetime.now().strftime('%Y-%m-%d %X')
            f = open(Logger.filename, "a")
            f.write(time + " " + pot_id + ": " + message + "\r\n")
            f.close()
        except IOError as e:
            print("Log file not accessible ", e)

    @staticmethod
    def purge():
        print("File exists:" + str(path.exists(Logger.filename)))
        print(Logger.filename)
        try:
            f = open(Logger.filename, "w")
            f.close()
        except IOError as e:
            print("Log file not accessible ", e)