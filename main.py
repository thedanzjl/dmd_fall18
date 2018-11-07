import sqlite3
db = sqlite3.connect('mydb')

cursor = db.cursor()
# example how to create tables
# cursor.execute('''
#         CREATE TABLE customers (cid INTEGER PRIMARY KEY,
#                                 username VARCHAR(30) NOT NULL,
#                                 full_name VARCHAR(40),
#                                 location VARCHAR(40),
#                                 phone_number VARCHAR(11),
#                                 email VARCHAR(40))
# ''')

username1 = 'name1'
full_name1 ='fullname1'
location1 = 'location1'
phone_number1 ='8805553535'
email1 = 'email1'

#how to insert info
# Insert cust 1
cursor.execute('''INSERT INTO customers(username, full_name, location, phone_number, email)
                  VALUES(?,?,?,?,?)''', (username1, full_name1,location1, phone_number1, email1))
print('First user inserted')

db.commit()
db.close()