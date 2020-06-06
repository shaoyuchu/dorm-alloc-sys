import flask
from flask import request
from flask import jsonify

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/api/get_all_identities', methods = ['GET', 'POST'])
def identityPool():
    if request.method == 'POST':
        result = ['post method']
        return jsonify(result)
    elif request.method == 'GET':
        result = ['get method']
        return jsonify(result)

if __name__ == '__main__':
    app.run()