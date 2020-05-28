import sqlite3

from flask import jsonify

from utility.sql.scripts_helper import ScriptsHelper
from utility.sql.macros_helper import MacrosHelper
from utility.sql.items_helper import ItemsHelper
from utility.sql.history_helper import HistoryHelper
from utility.sql.live_macros_helper import LiveMacrosHelper

from utility.current_date import get_current_date

from .invalid_usage import InvalidUsage


class MacrosHandler(object):
    def __init__(self, db):
        self._macros_helper = MacrosHelper(db)
        self._scripts_helper = ScriptsHelper(db)
        self._item_helper = ItemsHelper(db)
        self._history_helper = HistoryHelper(db)
        self._live_macros_helper = LiveMacrosHelper(db)

    def create_macro(self, user_id, request_json):
        keys = ["language", "local", "gender", "rules", "name"]

        for key in keys:
            if key not in request_json:
                return jsonify(message=f"{key} form is missing"), 400

        language = request_json["language"]
        local = request_json["local"]
        gender = request_json["gender"]
        rules = request_json["rules"]
        name = request_json["name"]
        note = request_json.get("note", "")

        row_id = -1
        current_date = get_current_date()

        try:
            row_id = self._item_helper.add_new_item("macro")

            self._macros_helper.add_macro(
                row_id, language, local, gender, rules, name, current_date
            )

            self._history_helper.add_new_record(
                user=user_id, action="Create", item_id=row_id, edit_time=current_date, note=note,
            )

            live_macro = self._live_macros_helper.get_live_macro_by_macro_name(
                name
            )

            if live_macro is None:
                self._live_macros_helper.init_new_version(name, row_id)
            else:
                self._live_macros_helper.select_new_version(macro_name=name, macro_id=row_id)

            self._history_helper.add_new_record(
                user=user_id, action="Set", item_id=row_id, edit_time=current_date,
            )

        except Exception as e:
            print(e)
            raise InvalidUsage("already got the same macro")

        return jsonify(id=row_id), 201

    def edit_macro(self, user_id, macro_id, request_json):
        keys = ["language", "local", "gender", "rules", "name"]

        for key in keys:
            if key not in request_json:
                return jsonify(message=f"{key} form missing"), 400

        language = request_json["language"]
        local = request_json["local"]
        gender = request_json["gender"]
        rules = request_json["rules"]
        name = request_json["name"]

        current_date = get_current_date()
        row_id = -1

        try:
            row_id = self._item_helper.add_new_item("macro")
            self._macros_helper.add_macro(
                row_id, language, local, gender, rules, name, current_date
            )

            self._live_macros_helper.select_new_version(macro_name=name, macro_id=row_id)

            self._history_helper.add_new_record(
                user=user_id, action="Create", item_id=row_id, edit_time=current_date
            )
        except Exception as e:
            print(e)
            raise InvalidUsage(f"cannot update {name}")

        return jsonify(id=row_id), 201

    def get_macro(self, macro_id):
        if macro_id is None:
            return "", 404

        macro = self._macros_helper.get_macro_by_macro_id(macro_id)

        if macro is None:
            return "", 404

        script_ids = macro["scripts"].split(",")
        scripts = []

        for script_id in script_ids:
            script = self._scripts_helper.get_script_by_script_id(script_id)
            scripts.append(script)

        return jsonify(macro={
          "name": macro["name"],
          "scripts": scripts,
          "language": macro["language"],
          "local": macro["local"],
          "gender": macro["gender"],
          })

    def get_languages(self):
        languages = self._macros_helper.get_all_language()
        return jsonify(languages=languages), 200

    def get_all_local_under_language(self, language):
        local = self._macros_helper.get_local_by_language(language)
        return jsonify(locals=local), 200

    def get_all_gender_under_language(self, language):
        gender = self._macros_helper.get_gender_by_language(language)
        return jsonify(genders=gender), 200

    def get_macros(self, language, local, gender):
        macros = self._macros_helper.get_macros(language, local, gender)
        return jsonify(macros=macros), 200

    def get_all_macros_by_name(self, name):
        macros = self._macros_helper.get_all_macros_by_name(macro_name=name)
        return jsonify(macros=macros), 200

    def delete_macro_by_macro_id(self, macro_id):
        is_live_macro = self._live_macros_helper.check_is_live_by_macro_id(macro_id)
        if is_live_macro:
          return jsonify(message="cannot delete macro because it is live macro"), 404
        else:
          try:
            self._macros_helper.delete_macro_by_macro_id(macro_id=macro_id)
            return "", 200
          except Exception as e:
            print(e)
            return "", 500