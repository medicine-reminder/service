import json
from flask import Flask
import flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy.sql import func
from json import JSONEncoder
from sqlalchemy import DateTime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meds.db'
db = SQLAlchemy(app)


@app.route('/meds/timestamps')
def meds():
    ret = meds.query.all()
    if(ret):
        returnArray = []
        for r in ret:
            returnArray.append(r.__toDateTime__())
        # print(json.dumps(returnArray))
        return flask.Response(json.dumps(returnArray))
    else:
        return '[]'

@app.route('/meds/led')
def meds_led():
    ret = meds.query.all()
    #print(ret)
    if(ret):
        # First define the two timespans
        first_timespan_beginning_hour = 6
        second_timespan_beginning_hour = 18
        isMorning = False

        timespan_beginning = None
        timespan_ending = None

        # decide - in which timespan are we now?
        now = datetime.now()
        if(now.hour < first_timespan_beginning_hour):
            timespan_beginning = datetime(now.year,now.month,now.day,6) - timedelta(hours=12)
            timespan_ending = datetime(now.year,now.month,now.day,6)
        elif(now.hour >= first_timespan_beginning_hour and now.hour < second_timespan_beginning_hour) :
            timespan_beginning = datetime(now.year,now.month,now.day,6)
            timespan_ending = datetime(now.year,now.month,now.day,6) + timedelta(hours=12)
        elif(now.hour > first_timespan_beginning_hour and now.hour >= second_timespan_beginning_hour) :
            timespan_beginning = datetime(now.year,now.month,now.day,18)
            timespan_ending = datetime(now.year,now.month,now.day,18) + timedelta(hours=12)

        print(timespan_beginning)
        print(timespan_ending)
        # iterate over the array of existing timestamps
        for r in ret:
            intake_datetime = r.intaketimestamp
            # check, weather a timestamp is in within the _now_ timespan
            if (intake_datetime > timespan_beginning and intake_datetime < timespan_ending):
                return 'False'

        return 'True'

    else:
        return 'True'

@app.route('/meds/taken')
def meds_taken():
    db.session.add(meds())
    db.session.commit()
    return 'True'

class meds(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    intaketimestamp = db.Column(DateTime(timezone=True))

    def __init__(self):
        self.intaketimestamp = datetime.now()

    def __toDateTime__(self):
        return self.intaketimestamp.isoformat()

db.create_all()
db.session.commit()