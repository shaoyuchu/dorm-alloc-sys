from .sqlite_connector import SQLiteConnector


class ScriptsHelper(object):
    def __init__(self, db):
        self._sql = SQLiteConnector(db)

    def get_script_by_script_id(self, script_id):
        self._sql.cursor.execute(
            """
                SELECT script_id, name, edit_time
                FROM scripts
                WHERE id = (?)
                """,
            (script_id,),
        )

        return self._sql.cursor.fetchone()

    def add_script(self, script_id, script_name, current_date):
        self._sql.cursor.execute(
            """
            INSERT INTO scripts (script_id, name, edit_time)
            VALUES (?, ?, ?)
            """,
            (script_id, script_name, current_date,),
        )
        self._sql.connector.commit()

    def get_all_scripts_by_name(self, name):
        self._sql.cursor.execute(
            """
            SELECT script_id, name, edit_time
            FROM scripts
            WHERE name = (?)
            """,
            (name,),
        )

        return self._sql.cursor.fetchall()

    def get_all_scripts(self):
        self._sql.cursor.execute(
            """
            SELECT DISTINCT name
            FROM scripts
            """
        )

        return self._sql.cursor.fetchall()

    def get_script_by_script_id(self, script_id):
        self._sql.cursor.execute(
            """
            SELECT script_id, name, edit_time
            FROM scripts
            WHERE script_id = (?)
            """,
            (script_id,),
        )

        return self._sql.cursor.fetchone()
