import flask
from flask import request
from flask import jsonify
from app import app

import sys
import pandas as pd
import numpy as np
from pandas.api.types import CategoricalDtype
from utility.static.Qua_config import *
from utility.Qua_mainFunc import *


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
        BoyInQua, GirlInQua, WaitDF = DivideDF(priority, student, beds)
        #still Work-in-progress
        BoyInQua, GirlInQua = Match(BoyInQua, GirlInQua, beds)
        CampusBoy, CampusGirl, BotBoy, BotGirl = GetOutputDF(priority, BoyInQua, GirlInQua, student, WaitDF)
        
        result = {
            "men_campus_dorm": CampusBoy,
            "women_campus_dorm": CampusGirl,
            "men_BOT": BotBoy,
            "women_BOT": BotGirl,
        }
        return jsonify(result)