from app import app
from flask import request

@app.route("/api/match", methods=["GET", "POST"])
def match():
    if request.method == "POST":
        return macros_handler.create_macro(request.get_json())
    else:
        language = request.args.get("language")
        local = request.args.get("local")
        gender = request.args.get("gender")
        macro_name = request.args.get("name")
        if macro_name is not None:
          return macros_handler.get_all_macros_by_name(name=macro_name)
        else:
          return macros_handler.get_macros(language, local, gender)