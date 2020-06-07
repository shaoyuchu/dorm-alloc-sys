import flask
from flask import request
from flask import jsonify
import json

import sys
import pandas as pd
import numpy as np
from pandas.api.types import CategoricalDtype
from Qua_config import *
from Qua_mainFunc import *

app = flask.Flask(__name__)

@app.route('/api/get_all_identities/', methods = ['POST'])
def identityPool():
    if request.method == 'POST':
        print('request', request)
        # print('request.json', request.json)
        student_data = request.json
        identity_pool = GetAllIdType(student_data)
        print('identity_pool', identity_pool)
        return jsonify(identity_pool)

@app.route('/api/match/', methods = ['POST'])
def result():
    if request.method == 'POST':
        print('request', request)
        # print('request.json', request.json)
        student = request.json['student']
        beds = request.json['beds']
        priority = request.json['priority']
        BoyInCam, GirlInCam, WaitDF = DivideDF(priority, student, beds)
        CampusBoy, CampusGirl, BotBoy, BotGirl = GetOutputDF(priority, BoyInCam, GirlInCam, student, WaitDF)
        result = {
            "men_campus_dorm": CampusBoy,
            "women_campus_dorm": CampusGirl,
            "men_BOT": BotBoy,
            "women_BOT": BotGirl,
        }
        return jsonify(result)

if __name__ == '__main__':
    app.run()