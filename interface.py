import sqlite3


class Database:

    def __init__(self, name):
        self.connection = sqlite3.connect(name, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.connection.cursor()

    def exec(self, query, *args):
        # try:
        self.cursor.execute(query, *args)
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
        EXAMPLE OF USE: insert_into('customers', username='hello132', name='Vasya', id=0)
        """
        values_names = str(tuple(kwargs.keys())).replace("'", "")
        q_signs = (',?' * len(kwargs))[1:]
        self.exec('''insert into {}{} values ({})'''.format(table_name, values_names, q_signs), tuple(kwargs.values()))

    def clear_all(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        names = self.cursor.fetchall()
        for name in names:
            self.exec("DELETE FROM {}".format(name[0]))

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
