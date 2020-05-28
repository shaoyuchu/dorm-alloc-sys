from __main__ import app
from flask import request
from handler.macros_handler import MacrosHandler

db = "./db/metagraph_development.db" if app.debug else "./db/metagraph_production.db"
macros_handler = MacrosHandler(db)


@app.route("/api/macros/<macro_id>", methods=["GET", "PUT", "DELETE"])
def macros_with_macro_id(macro_id):
    if request.method == "GET":
        return macros_handler.get_macro(macro_id)
    elif request.method == "PUT":
        user_id = request.cookies.get("USER_ID", "Anonymous")

        return macros_handler.edit_macro(user_id, macro_id, request.get_json())
    else:
        return macros_handler.delete_macro_by_macro_id(macro_id)

@app.route("/api/macros", methods=["GET", "POST"])
def macros():
    if request.method == "POST":
        user_id = request.cookies.get("USER_ID", "Anonymous")

        return macros_handler.create_macro(user_id, request.get_json())
    else:
        language = request.args.get("language")
        local = request.args.get("local")
        gender = request.args.get("gender")
        macro_name = request.args.get("name")

        if macro_name is not None:
          return macros_handler.get_all_macros_by_name(name=macro_name)
        else:
          return macros_handler.get_macros(language, local, gender)


@app.route("/api/macros/languages", methods=["GET"])
def macros_language():
    return macros_handler.get_languages()


@app.route("/api/macros/<language>/locals", methods=["GET"])
def macro_local(language):
    return macros_handler.get_all_local_under_language(language)


@app.route("/api/macros/<language>/genders", methods=["GET"])
def macro_gender(language):
    return macros_handler.get_all_gender_under_language(language)
