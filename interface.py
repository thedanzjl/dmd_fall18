import sqlite3


class Database:

    def __init__(self, name):
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()

    def exec(self, query):
        # try:
        self.cursor.execute(query)
        self.connection.commit()
        # except:
        #     self.connection.rollback()

    def query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)

        return cursor.fetchall()

    def insert_into(self, table_name, **kwargs):
        """
        :param kwargs: listed attributes to be inserted into table.
        :param table_name: name of table in string format
        EXAMPLE OF USE: insert_into('customers', username='hello132', name='Vacya', id=0)
        """
        insert_statement = """INSERT INTO {}{} VALUES {}""".format(
            table_name, str(tuple(kwargs.keys())).replace("'", ""), tuple(kwargs.values()))
        self.exec(insert_statement)

    def clear_all(self):
        self.exec("DELETE FROM customers")
        self.exec("DELETE FROM rides")
        self.exec("DELETE FROM cars")
        self.exec("DELETE FROM plug_types")
        self.exec("DELETE FROM charging_stations")
        self.exec("DELETE FROM car_part_types")
        self.exec("DELETE FROM providers")
        self.exec("DELETE FROM workshops")

    def clear(self, table_name):
        self.exec("DELETE FROM {}".format(table_name))

    def __del__(self):
        self.connection.close()


if __name__ == "__main__":
    db = Database('test.sqlite')

    # CleanUp Operation
    del_query = "DELETE FROM basic_python_database"
    db.exec(del_query)

    # Data Insert into the table
    query = """
            INSERT INTO basic_python_database
            (`name`, `age`)
            VALUES
            ('Mike', 21),
            ('Michael', 21),
            ('Imran', 21)
            """

    # db.query(query)
    db.insert(query)

    # Data retrieved from the table
    select_query = """
            SELECT * FROM basic_python_database
            WHERE age = 21
            """

    people = db.query(select_query)

    for person in people:
        print("Found ? " % person['name'])
