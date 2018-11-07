import sqlite3
db = sqlite3.connect('mydb')

cursor = db.cursor()
cursor.execute('''
        CREATE TABLE customers (cid INTEGER PRIMARY KEY,
                                username VARCHAR(30) NOT NULL,
                                full_name VARCHAR(40),
                                location VARCHAR(40),
                                phone_number VARCHAR(11),
                                email VARCHAR(40))
''')
db.commit()
db.close()