#!/usr/bin/env python3
import sqlalchemy as sa
from sqlalchemy import create_engine, text

class SqlLiteDatabase: 
    def __init__(self):
        self.engine = create_engine("sqlite+pysqlite:///:memory:", future=True)

    def _test_connect(self, test_text: str) -> sa.engine.cursor.CursorResult:
        """test connection to in-memory db

        Args:
            input (str): test message you wanna see echoed after db connect

        Returns:
            sqlalchemy.engine.cursor.CursorResult: returns select output 
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(f"select '{test_text}'"))
        return result

    def _check_for_table(self, target_table: str) -> bool:
        """check for existing table in

        Args:
            target_table (str): table you want to check for

        Returns:
            bool: whether or not table exists
        """
        inspect = sa.inspect(self.engine)
        has_table = inspect.has_table(target_table)
        return has_table


    def insert_table_tuple(self, table_name: str, table_contents: tuple):
        """insert table and create if necessary

        Args:
            table_name (str): name of target table
            table_contents (tuple): coordinates
        """
        has_table = self._check_for_table(table_name)
        with self.engine.begin() as conn:
            if not has_table:
                conn.execute(text(f"CREATE TABLE {table_name} (x int, y int)"))
            conn.execute(text(f"INSERT INTO {table_name} (x,y) VALUES (:x, :y)"),
                [{"x": table_contents[0], "y": table_contents[1]}]
            )

    def fetch_table_contents(self, table_name: str) -> sa.engine.cursor.CursorResult:
        has_table = self._check_for_table(table_name) 
        with self.engine.connect() as conn:
            if has_table:
                return conn.execute(text(f"select x, y FROM {table_name}"))

    def print_table_rows(self, cursor: sa.engine.cursor.CursorResult):
        print([f"x: {row.x} y: {row.y}" for row in cursor])



def main():
    print('creating test_db')
    test_db = SqlLiteDatabase()
    print('testing_connection')
    test_db._test_connect("test")
    print('creating plot table')
    test_db.insert_table_tuple("coords", (1, 2))
    test_db.insert_table_tuple("coords", (2, 4))
    coords = test_db.fetch_table_contents("coords")
    test_db.print_table_rows(coords)


if __name__ == "__main__":
    main()
