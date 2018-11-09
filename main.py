import sqlite3
db = sqlite3.connect('mydb.db')

cursor = db.cursor()

#так это можно закоментить и удобно, но надо сделать общую функцию "добавить таблицу" (наверное)
def init_db():
    cursor.execute('''
        CREATE TABLE customers (
            cid INTEGER PRIMARY KEY,                                 
            username VARCHAR(30) NOT NULL,                                 
            full_name VARCHAR(40),
            location VARCHAR(40),
            phone_number VARCHAR(11),
            email VARCHAR(40))                              
    ''')

    cursor.execute('''
        CREATE TABLE rides (
            rid INTEGER PRIMARY KEY,
            initial_location VARCHAR(40),
            destination VARCHAR(40))                            
    ''')

    cursor.execute('''
        CREATE TABLE cars (
            carid INTEGER PRIMARY KEY,
            current_state VARCHAR(20),
            battery_level INTEGER,
            location VARCHAR(40))                          
    ''')

    cursor.execute('''
        CREATE TABLE plug_types (
            ptid INTEGER PRIMARY KEY,
            shape VARCHAR(20),
            size INTEGER)                        
    ''')

    cursor.execute('''
        CREATE TABLE charging_stations (
            csid INTEGER PRIMARY KEY,
            location VARCHAR(40),
            price INTEGER,
            plug_types VARCHAR(40),
            time_of_charging_min INTEGER,
            amount_of_sockets INTEGER)                     
    ''')

    cursor.execute('''
        CREATE TABLE car_part_types (
            cpid INTEGER PRIMARY KEY,
            price INTEGER)                   
    ''')

    cursor.execute('''
        CREATE TABLE providers (
            pid INTEGER PRIMARY KEY,
            name VARCHAR(20) NOT NULL,
            phone_number VARCHAR(11),
            location VARCHAR(40))                
    ''')

    cursor.execute('''
        CREATE TABLE workshops (
            wid INTEGER PRIMARY KEY,
            name VARCHAR(20),
            location VARCHAR(40),
            availability VARCHAR(20),
            price_in_hours INTEGER)             
    ''')

#можно так но лучше в класс оформить, по человечески (наверное)

def add_customer(username, full_name, location, phone_number, email):
    cursor.execute("INSERT INTO customers(username, full_name, location, phone_number, email) VALUES ('%s','%s','%s','%s','%s')"%(username, full_name, location, phone_number, email))
    db.commit()
    print('+customer')


# cursor.execute('''INSERT INTO customers(username, full_name, location, phone_number, email)
#                   VALUES(username1, full_name1,location1, 88005553535, email1)''')
# print('First user inserted')

init_db()
add_customer('u1','fn1','l1','1','e1')

db.close()