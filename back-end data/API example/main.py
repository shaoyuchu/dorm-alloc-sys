import argparse

from flask import Flask
from flask_cors import CORS
from utility.get_upload_folders import get_upload_folders

app = Flask(__name__)

app.config["JSON_AS_ASCII"] = False
app.config["UPLOAD_FOLDER"] = get_upload_folders()

cors = CORS(app,
            resources={r"/api/*": {"origins": ["http://localhost/*", "https://localhost/*"]}},
            headers=['Content-Type', 'Authorization'],
            expose_headers='Authorization')

def import_router():
    import router.token_verification
    import router.error_router
    import router.transcribe_router
    import router.scripts_router
    import router.live_scripts_router
    import router.live_macros_router
    import router.macros_router
    import router.history_router


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args() 

    if args.debug:
        app.debug = True

    import_router()

    app.run(debug=app.debug)
