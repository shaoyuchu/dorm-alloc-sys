import flask
from flask import request
from flask import jsonify
import json
import argparse
from app import app


def import_router():
    import router.router

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", default="-d", action="store_true")
    args = parser.parse_args() 
    
    if args.debug:
        app.debug = True

    import_router()
    app.run(debug=app.debug)