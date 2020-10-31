import numpy as np
import json
import logging
import flask
import os

from sessions import create_new_session, end_session, get_session_data, insert_session_data
import sys
sys.path.append("../")
from elicit import ElectoralElicitation


app = flask.Flask(__name__)


def option_to_string(option: int):
    if option == 1:
        return "Option 1: Winner Takes All"
    elif option == 2:
        return "Option 2: Split-Vote"
    else:
        return "ERROR"


def generate_vote_data(ee: ElectoralElicitation):
    vd = ee.generate_trial()
    states = ['Vermont', 'Ohio', 'South Dakota', 'Alaska', 'Michigan', 'Oklahoma', 'Mississippi', 'Virginia', 'Texas', 'Arkansas', 'Utah', 'Connecticut', 'Delaware', 'Florida', 'Indiana', 'Maryland', 'New Hampshire', 'Arizona', 'New Mexico', 'Nebraska', 'Kansas', 'Louisiana', 'Tennessee', 'Maine', 'Rhode Island', 'Colorado', 'Idaho', 'North Carolina', 'Georgia', 'Kentucky', 'New Jersey', 'West Virginia', 'Massachusetts', 'Iowa', 'Hawaii', 'Washington', 'Alabama', 'Wisconsin', 'California', 'North Dakota', 'Pennsylvania', 'Wyoming', 'South Carolina', 'New York', 'Illinois', 'Minnesota', 'Montana', 'Nevada', 'Missouri', 'Oregon']
    vd_dict = dict()
    for i in range(50):
        s = states[i].upper()
        vd_dict[s] = {
            "h": vd.stoh[i],
            "dv": vd.stodv[i],
        }
    return vd_dict, vd


@app.route('/', methods=['GET', 'POST'])
def home():
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
        
        if 'sid' not in flask.session:
            resp = flask.make_response("Error: never started the survey", 400)
            return resp
 
        sid = flask.session['sid']
        ret = get_session_data(sid)
        ee = ret[0]
        cur_vd = ret[1]
        if data["winner"] == "D":
            ee.process_trial(cur_vd, True)
        else:
            ee.process_trial(cur_vd, False)

        if ee.converged():
            o_hat = ee.predict_opt()
            o_hat_str = option_to_string(o_hat)
            f_hat = round(ee.predict_f(), 2)
            return json.dumps(
                {
                    'option': o_hat_str,
                    'fairness': f_hat,
                }
            )

        vd_dict, cur_vd = generate_vote_data(ee)
        ret[-1] = cur_vd # update stored vd
        return json.dumps(vd_dict)

    # start a new session
    sid = create_new_session()
    flask.session['sid'] = sid
    ee = ElectoralElicitation(50) 
    vd_dict, cur_vd = generate_vote_data(ee)
    insert_session_data(sid, [ee, cur_vd])

    fp = open('shapes/usa2.json', 'rb')
    context = {
        'vote_data': vd_dict,
        'map_json': json.load(fp),

    }
    fp.close()
    return flask.render_template('map_view.html', **context)


app.secret_key = 'yeet'


# run the app.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)

