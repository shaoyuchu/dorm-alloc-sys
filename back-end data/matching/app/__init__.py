import redis

from flask import Flask
from flask_cors import CORS
from rq import Queue

from utility.get_upload_folders import get_upload_folders


app = Flask(__name__)
r = redis.Redis()
q = Queue(connection=r)

app.config["JSON_AS_ASCII"] = False
app.config["UPLOAD_FOLDER"] = get_upload_folders()

cors = CORS(app,
            resources={r"/api/*": {"origins": ["http://localhost/*", "https://localhost/*"]}},
            headers=['Content-Type', 'Authorization'],
            expose_headers='Authorization')