import argparse

from flask import Flask
from flask_cors import CORS
from utility.get_upload_folders import get_upload_folders

from middleware.middleware import Middleware

from app import app

def import_router():
    import router.error_router
    import router.transcribe_router
    import router.scripts_router
    import router.live_scripts_router
    import router.live_macros_router
    import router.macros_router
    import router.history_router
    import router.jobs_router

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args() 

    if args.debug:
        app.debug = True

    import_router()

    app.wsgi_app = Middleware(app.wsgi_app, app.debug)
    
    app.run(debug=app.debug)
