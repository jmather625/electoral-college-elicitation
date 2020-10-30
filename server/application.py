import numpy as np
import json
import logging
import flask

import sys
sys.path.append("../")
from common import VoterData, get_random_dv, get_random_hs, HOUSE_REP_TO_POP
from elicit import Option2Elicit


application = flask.Flask(__name__)


# using global for now
o2e = Option2Elicit(50)
cur_trial = None


def generate_vote_data():
    global o2e, cur_trial
    vd = o2e.generate_trial()
    cur_trial = vd
    states = ['Vermont', 'Ohio', 'South Dakota', 'Alaska', 'Michigan', 'Oklahoma', 'Mississippi', 'Virginia', 'Texas', 'Arkansas', 'Utah', 'Connecticut', 'Delaware', 'Florida', 'Indiana', 'Maryland', 'New Hampshire', 'Arizona', 'New Mexico', 'Nebraska', 'Kansas', 'Louisiana', 'Tennessee', 'Maine', 'Rhode Island', 'Colorado', 'Idaho', 'North Carolina', 'Georgia', 'Kentucky', 'New Jersey', 'West Virginia', 'Massachusetts', 'Iowa', 'Hawaii', 'Washington', 'Alabama', 'Wisconsin', 'California', 'North Dakota', 'Pennsylvania', 'Wyoming', 'South Carolina', 'New York', 'Illinois', 'Minnesota', 'Montana', 'Nevada', 'Missouri', 'Oregon']
    vote_data = dict()
    for i in range(50):
        s = states[i].upper()
        vote_data[s] = {
            "h": vd.stoh[i],
            "dv": vd.stodv[i],
        }
    return vote_data


@application.route('/', methods=['GET', 'POST'])
def home():
    global o2e, cur_trial
    if flask.request.method == 'POST':
        data = None
        try:
            data = json.loads(flask.request.get_data())
        except:
            logging.error("Error could not parse JSON", exc_info=True)
            resp = flask.make_response("Error: could not parse JSON", 400)
            return resp
        if "winner" not in data or data["winner"] not in ["D", "R"]:
            logging.error("Invalid payload")
            resp = flask.make_response("Error: invalid payload", 400)
            return resp

        if data["winner"] == "D":
            o2e.process_trial(cur_trial, True)
        else:
            o2e.process_trial(cur_trial, False)

        if o2e.converged:
            f_hat = o2e.predict_f()
            o2e.clear()
            return json.dumps(
                {'fairness': f_hat}
            )

        vote_data = generate_vote_data()
        return json.dumps(vote_data)

        
    vote_data = generate_vote_data()
    fp = open('shapes/usa2.json', 'rb')
    context = {
        'vote_data': vote_data,
        'map_json': json.load(fp),

    }
    fp.close()
    return flask.render_template('map_view.html', **context)


# run the application.
if __name__ == "__main__":
    application.debug = True
    application.run(host="0.0.0.0", threaded=True)

