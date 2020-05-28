import os
import pathlib
import sqlite3

from flask import jsonify

from werkzeug.utils import secure_filename

from utility.get_upload_folders import get_upload_folders
from utility.sql.scripts_helper import ScriptsHelper
from utility.sql.live_scripts_helper import LiveScriptsHelper
from utility.sql.items_helper import ItemsHelper
from utility.sql.history_helper import HistoryHelper
from utility.sql.macros_helper import MacrosHelper

from utility.current_date import get_current_date

from .invalid_usage import InvalidUsage
from .helper import attach_date_to_script_name

ALLOWED_EXTENSIONS = {"tsv"}


class ScriptsHander(object):
    def __init__(self, db):
        self._scripts_helper = ScriptsHelper(db)
        self._live_scripts_helper = LiveScriptsHelper(db)
        self._item_helper = ItemsHelper(db)
        self._history_helper = HistoryHelper(db)
        self._macros_helper = MacrosHelper(db)

    def _allowed_script(self, script_name):
        return "." in script_name and script_name.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

    def _save_script(self, script, script_name, script_path, current_date):
        pathlib.Path(script_path).mkdir(parents=True, exist_ok=True)
        split_array = script_name.split(".")

        script_name_with_date = split_array[0] + " " + current_date + "." + split_array[1]

        script.save(os.path.join(script_path, script_name_with_date))

    def _store_script_information(self, script_id, script_name, current_date):
        self._scripts_helper.add_script(script_id, script_name, current_date)

    def get_all_scripts_by_script_name(self, script_name):
        scripts = None
        if script_name is None:
            scripts = self._scripts_helper.get_all_scripts()
        else:
            scripts = self._scripts_helper.get_all_scripts_by_name(script_name)

        return jsonify(scripts=scripts)

    def get_script_by_script_id(self, script_id):
      return jsonify(script=self._scripts_helper.get_script_by_script_id(script_id))

    def get_script_path(self, script_id):
        script = self._scripts_helper.get_script_by_script_id(script_id)

        upload_path = get_upload_folders()
        script_name_with_date = attach_date_to_script_name(script)

        upload_path += script_name_with_date

        return upload_path

    def _upload_script(self, user_id, script, note):
        script_name = secure_filename(script.filename)
        script_path = get_upload_folders() + "/scripts/" + script_name

        current_date = get_current_date()

        self._save_script(script, script_name, script_path, current_date)
        row_id = -1

        try:
            row_id = self._item_helper.add_new_item("script")
            self._store_script_information(row_id, script_name, current_date)
            current_live_script = self._live_scripts_helper.get_live_scripts_by_script_name(
                script_name
            )

            self._history_helper.add_new_record(
                user=user_id, action="Upload", item_id=row_id, edit_time=current_date, note=note,
            )

            if current_live_script is None:
                self._live_scripts_helper.init_new_version(script_name, row_id)
            else:
                self._macros_helper.update_to_latest_script(current_live_script["script_id"], row_id)
                self._live_scripts_helper.select_new_version(script_name=script_name, script_id=row_id)

            self._history_helper.add_new_record(
                user=user_id, action="Set", item_id=row_id, edit_time=current_date,
            )
            return {"id": row_id}
        except Exception as e:
            print(e)
            raise InvalidUsage("already got the same scripts")

    def upload_scripts(self, user_id, scripts, note):
        if scripts is None or len(scripts) == 0:
            raise InvalidUsage("please upload script")

        script_ids = []

        for script in scripts:
            if script and self._allowed_script(script.filename):
                script_id = self._upload_script(user_id=user_id, script=script, note=note)
                script_ids.append(script_id)

            else:
                raise InvalidUsage("Only support tsv format script")

        return jsonify(scripts=script_ids), 201
