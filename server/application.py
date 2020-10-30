import numpy as np
import json
from flask import Flask, render_template

import sys
sys.path.append("../")
from common import VoterData, get_random_dv, get_random_hs, HOUSE_REP_TO_POP


application = Flask(__name__)


def get_vote_data():
    np.random.seed(7)

    ns = 50
    stop = []
    stoh = []
    stodv = []
    for _ in range(ns):
        dv = get_random_dv()
        hs = get_random_hs()
        stodv.append(dv)
        stoh.append(hs)
        stop.append(hs * HOUSE_REP_TO_POP)
    vd = VoterData(ns, stop, stoh, stodv)

    states = ['Vermont', 'Ohio', 'South Dakota', 'Alaska', 'Michigan', 'Oklahoma', 'Mississippi', 'Virginia', 'Texas', 'Arkansas', 'Utah', 'Connecticut', 'Delaware', 'Florida', 'Indiana', 'Maryland', 'New Hampshire', 'Arizona', 'New Mexico', 'Nebraska', 'Kansas', 'Louisiana', 'Tennessee', 'Maine', 'Rhode Island', 'Colorado', 'Idaho', 'North Carolina', 'Georgia', 'Kentucky', 'New Jersey', 'West Virginia', 'Massachusetts', 'Iowa', 'Hawaii', 'Washington', 'Alabama', 'Wisconsin', 'California', 'North Dakota', 'Pennsylvania', 'Wyoming', 'South Carolina', 'New York', 'Illinois', 'Minnesota', 'Montana', 'Nevada', 'Missouri', 'Oregon']
    vote_data = dict()
    for i in range(50):
        s = states[i].upper()
        vote_data[s] = {
            "h": vd.stoh[i],
            "dv": vd.stodv[i],
        }
    return vote_data


@application.route('/')
def home():
    vote_data = get_vote_data()

    fp = open('shapes/usa2.json', 'rb')
    context = {
        'vote_data': vote_data,
        'map_json': json.load(fp),

    }
    fp.close()
    return render_template('map_view.html', **context)


# run the application.
if __name__ == "__main__":
    application.debug = True
    application.run(host="0.0.0.0", threaded=True)

