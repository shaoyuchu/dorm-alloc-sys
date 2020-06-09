import flask
from flask import request
from flask import jsonify

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/api/get_all_identities/', methods = ['GET', 'POST'])
def identityPool():
    if request.method == 'POST':
        print('request', request)
        print('request.json', request.json)
        return jsonify([
            '港澳生',
            '本國生',
            '原住民族籍',
            '外籍生',
            '外交人員子女學生',
            '僑生',
            '陸生',
            '交換生',
            '公費生',
            '奧林匹亞',
            '身心障礙',
            '離島地區生',
            '低收入戶',
            '中低收入戶',
        ])
    elif request.method == 'GET':
        print('request.args', request.args)
        return jsonify(['get method'])

@app.route('/api/match/', methods = ['GET', 'POST'])
def result():
    if request.method == 'POST':
        print('request', request)
        print('request.json', request.json)
        return jsonify({
            "men_campus_dorm": [
                []
            ],
            "women_campus_dorm": [
                []
            ],
            "men_BOT":[
                []
            ],
            "women_BOT":[
                []
            ],
        })
    elif request.method == 'GET':
        print('request.args', request.args)
        return jsonify(['get method'])

if __name__ == '__main__':
    app.run()