from __main__ import app
from flask import request, send_file

from handler.scripts_handler import ScriptsHander
from handler.invalid_usage import InvalidUsage

db = "./db/metagraph_development.db" if app.debug else "./db/metagraph_production.db"
scripts_hander = ScriptsHander(db)


@app.route("/api/scripts", methods=["GET", "POST"])
def scripts():
    if request.method == "POST":
        user_id = request.cookies.get("USER_ID", "Anonymous")
        note = request.form.get("note", "")
        scripts = request.files.getlist("scripts[]")

        return scripts_hander.upload_scripts(user_id, scripts, note)
    else:
        script_name = request.args.get("script_name")
        return scripts_hander.get_all_scripts_by_script_name(script_name)

@app.route("/api/scripts/<script_id>", methods=["GET"])
def get_script_by_script_id(script_id):
  return scripts_hander.get_script_by_script_id(script_id)

@app.route("/api/scripts/download/<script_id>", methods=["GET"])
def download_scripts_by_script_id(script_id):
    path = scripts_hander.get_script_path(script_id)
    return send_file(path, as_attachment=True)
