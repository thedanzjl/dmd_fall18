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

    def query(self, query, *args):
        cursor = self.connection.cursor()
        cursor.execute(query, *args)

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

    def get_tables_names(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        names = self.cursor.fetchall()
        return list(map(lambda x: x[0], names))

    def get_table_info(self, table_name):
        columns = self.query('''PRAGMA table_info({});'''.format(table_name))
        return columns

    def clear_all(self):
        names = self.get_tables_names()
        for name in names:
            self.exec("DELETE FROM {}".format(name))

    def clear(self, table_name):
        self.exec("DELETE FROM {}".format(table_name))

    def __del__(self):
        self.connection.close()


def intro(func):
    """
    Wrapper function that introduces function name and prints its result
    """

    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is not None:
            print(func.__name__, ': ')
            print(result)
        return result

    return inner


class MyDate:

    def __init__(self, y, m, d):
        self.y = y
        self.m = m
        self.d = d

    def __str__(self):
        return '{:4}-{:02}-{:02}'.format(self.y, self.m, self.d)

