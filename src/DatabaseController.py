from typing import List, Optional, Union
import sqlite3


class DatabaseController:
    def __init__(self, database: str) -> None:
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.close()

    def create_table(self, table_name: str, values: str) -> None:
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + table_name + " (" + values + ");")
        self.connection.commit()

    def delete_table(self, table_name: str) -> None:
        self.cursor.execute("DROP TABLE " + table_name + ";")
        self.connection.commit()

    def get_table(self, table_name: str) -> List[List[Optional[Union[str, int]]]]:
        self.cursor.execute("SELECT * FROM " + table_name + ";")
        return self.cursor.fetchall()

    def get_line(self, table_name: str, line_key: str) -> List[List[Optional[Union[str, int]]]]:
        self.cursor.execute("SELECT * FROM " + table_name + " WHERE " + line_key + ";")
        return self.cursor.fetchall()

    def get_value(self, table_name: str, key_to_value: str, key_to_line: str) -> Optional[Union[str, int]]:
        self.cursor.execute("SELECT " + key_to_value + " FROM " + table_name + " WHERE " + key_to_line)
        return self.cursor.fetchall()

    def add_line(self, table_name: str, keys: str, values: str) -> None:
        self.cursor.execute("INSERT INTO " + table_name + " " + keys + " VALUES(" + values + ");")
        self.connection.commit()

    def update_line(self, table_name: str, values: str, keys: str) -> None:
        self.cursor.execute("UPDATE " + table_name + " SET " + values + " WHERE " + keys + ";")
        self.connection.commit()

    def delete_line(self, table_name: str, key: str) -> None:
        self.cursor.execute("DELETE FROM " + table_name + " WHERE " + key + ";")
        self.connection.commit()

    def close(self) -> None:
        self.connection.commit()
        self.connection.close()


if __name__ == '__main__':
    pass
