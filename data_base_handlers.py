import sqlite3


class Database:
    """Class initialization"""

    def __init__(self, name: str):
        self.connection = sqlite3.connect(name + ".db")
        self.cursor = self.connection.cursor()

    def read_tables(self):
        """Returns all tables"""
        self.cursor.execute('''
            SELECT 
                *
            FROM 
                sqlite_schema

        ''')
        rows = self.cursor.fetchall()
        return rows

    def read_table(self, name, columns="*", condition=1):
        """Returns the table and writes in the variable "rows"""
        self.cursor.execute(f"SELECT {columns} FROM {name} WHERE {condition}")
        rows = self.cursor.fetchall()
        return rows

    def read_table_headers(self, name):
        """Returns the name of the table columns"""
        self.cursor.execute(f"PRAGMA table_info({name})")
        raw = self.cursor.fetchall()
        return [record[1:3] for record in raw]

    def create_table(self, name, columns: dict):
        """Creating a table with columns name"""
        columns_data = ", ".join(column_name + " " + columns[column_name] for column_name in columns)
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {name} ({columns_data})")

    def add_record(self, table_name, values: tuple):
        """ creates a row in table 'name' inserting each value in respective column"""
        query = f"INSERT INTO {table_name} VALUES {values}"
        self.cursor.execute(query)

    def update_records(self, table, changes, condition=""):
        """makes changes in table rows that fit condition. Implements changes massively if condition is default """
        query = f"UPDATE {table} SET {changes} {condition}"
        print(query)
        self.cursor.execute(query)

    def delete_table(self, table):
        """Removing the table"""
        self.cursor.execute(f"DROP TABLE {table}")
        # self.save()

    def delete_records(self, table, condition):
        """delete table row(s) that fit condition"""
        self.cursor.execute(f"DELETE FROM {table} WHERE {condition}")

    def add_column(self, table_name: str, column: tuple, _index: int = -1):
        """Adding one column to the table"""
        table = self.read_table(table_name)
        table_headers = self.read_table_headers(table_name)
        self.delete_table(table_name)
        if _index == -1:
            table_headers.append(column)
        else:
            table_headers.insert(_index, column)
        print(table_headers)
        dic_table_headers = {header[0]: header[1] for header in table_headers}
        self.create_table(table_name, dic_table_headers)
        for row in table:
            new_row = list(row)
            new_row.insert(_index, None)
            new_row = tuple(new_row)
            self.add_record(table_name, new_row)
        return f"column {column[0]} is added"

    def delete_column(self, table_name: str, column_name: str):
        """Removing one column in the table"""
        table_headers = self.read_table_headers(table_name)
        self.delete_table(table_name)
        index_column = table_headers.index(column_name)
        table_headers.pop(index_column)
        dic_table_headers = {header[0]: header[1] for header in table_headers}
        self.create_table(table_name, dic_table_headers)
        return f"column {column_name} is deleted"

    # def add_values_column(self, table_name: str, column, values):
    #     pass

    def save(self):
        """Preservation of changes in long -term memory"""
        self.connection.commit()


def str_to_list(value):
    """Converting from text to list"""
    return [int(i) for i in value.split(",")]


def list_to_str(array):
    """Converting from list to text"""
    return ", ".join(str(i) for i in array)


if __name__ == "__main__":
    db1 = Database("data_base")
