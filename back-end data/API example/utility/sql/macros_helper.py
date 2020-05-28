from .sqlite_connector import SQLiteConnector


class MacrosHelper(object):
    def __init__(self, db):
        self._sql = SQLiteConnector(db)

    def add_macro(self, macro_id, language, local, gender, scripts, name, edit_time):
        self._sql.cursor.execute(
            """
              INSERT INTO Macros (macro_id, language, local, gender, scripts, name, edit_time)
              VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (macro_id, language, local, gender, scripts, name, edit_time,),
        )

        self._sql.connector.commit()

    def update_macros(self, language, local, gender, scripts, name, macro_id, edit_time):
        self._sql.cursor.execute(
            """
              UPDATE macros
              SET language = (?),
                  local = (?),
                  gender = (?),
                  scripts = (?),
                  name = (?),
                  edit_time = (?)

              WHERE macro_id = (?)
            """,
            (language, local, gender, scripts, name, edit_time, macro_id,),
        )

        self._sql.connector.commit()

    def update_to_latest_script(self, old_script_id, new_script_id):
        self._sql.cursor.execute(
            """
            UPDATE Macros
            SET scripts = REPLACE(scripts, (?), (?))
          """,
            (str(old_script_id), str(new_script_id),),
        )

        self._sql.connector.commit()

    def get_macro_by_macro_id(self, macro_id):
        self._sql.cursor.execute(
            """
              SELECT name, scripts, language, local, gender
              FROM   macros
              WHERE  macro_id = (?)
            """,
            (macro_id,),
        )

        return self._sql.cursor.fetchone()

    def get_all_language(self):
        self._sql.cursor.execute(
            """
              SELECT DISTINCT Macros.language
              FROM   Macros INNER JOIN LiveMacros
              ON Macros.macro_id = LiveMacros.macro_id
            """
        )

        return self._sql.cursor.fetchall()

    def get_all_macros_by_name(self, macro_name):
        self._sql.cursor.execute(
          """
          SELECT *
          FROM Macros
          WHERE name = (?)
          """,
          (macro_name,),
        )

        return self._sql.cursor.fetchall()

    def get_local_by_language(self, language):
        self._sql.cursor.execute(
            """
          SELECT DISTINCT Macros.local
          FROM   Macros INNER JOIN LiveMacros
          ON Macros.macro_id = LiveMacros.macro_id
          WHERE language = (?)
          """,
            (language,),
        )

        return self._sql.cursor.fetchall()

    def get_gender_by_language(self, language):
        self._sql.cursor.execute(
            """
          SELECT DISTINCT Macros.gender
          FROM   Macros INNER JOIN LiveMacros
          ON Macros.macro_id = LiveMacros.macro_id
          WHERE language = (?)
          """,
            (language,),
        )
        return self._sql.cursor.fetchall()

    def get_macros(self, language, local, gender):
        self._sql.cursor.execute(
            """
          SELECT Macros.macro_id, Macros.name
          FROM Macros INNER JOIN LiveMacros
          ON Macros.macro_id = LiveMacros.macro_id
          WHERE language = (?) AND local = (?) AND gender = (?)
          """,
            (language, local, gender),
        )

        return self._sql.cursor.fetchall()

    def delete_macro_by_macro_id(self, macro_id):
        self._sql.cursor.execute(
          """
          DELETE
          FROM Macros
          WHERE macro_id = (?)
          """,
          (macro_id,),
        )

        self._sql.connector.commit()