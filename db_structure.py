
from interface import Database
db = Database('db.sqlite')

# ----CREATING TABLES----

db.exec("PRAGMA foreign_keys=ON")
db.exec('''
    CREATE TABLE IF NOT EXISTS customers (
        cid INTEGER PRIMARY KEY,                                 
        username VARCHAR(30) UNIQUE NOT NULL,                                 
        full_name VARCHAR(40),
        location VARCHAR(40),
        phone_number VARCHAR(11),
        email VARCHAR(40))                              
''')

db.exec('''
    CREATE TABLE IF NOT EXISTS rides (
        rid INTEGER PRIMARY KEY,
        initial_location VARCHAR(40),
        destination VARCHAR(40),
        carid INTEGER UNIQUE, 
        cid INTEGER UNIQUE,
        FOREIGN KEY (carid) REFERENCES cars(carid),
        FOREIGN KEY (cid) REFERENCES customers(cid)
        )
''')

db.exec('''
    CREATE TABLE IF NOT EXISTS cars (
        carid INTEGER PRIMARY KEY,
        current_state VARCHAR(20),
        battery_level INTEGER,
        location VARCHAR(40), 
        ptid INTEGER,
        FOREIGN KEY (ptid) REFERENCES plug_types(ptid))                          
''')

db.exec('''
    CREATE TABLE IF NOT EXISTS plug_types (
        ptid INTEGER PRIMARY KEY,
        shape VARCHAR(20),
        size INTEGER)                  
''')

db.exec('''
    CREATE TABLE IF NOT EXISTS charging_stations (
        csid INTEGER PRIMARY KEY,
        location VARCHAR(40),
        price INTEGER,
        plug_types VARCHAR(40),
        time_of_charging_min INTEGER,
        amount_of_sockets INTEGER)                     
''')

db.exec('''
    CREATE TABLE IF NOT EXISTS car_part_types (
        cpid INTEGER PRIMARY KEY,
        price INTEGER)                   
''')

db.exec('''
    CREATE TABLE IF NOT EXISTS providers (
        pid INTEGER PRIMARY KEY,
        name VARCHAR(20) NOT NULL,
        phone_number VARCHAR(11),
        location VARCHAR(40)
        )                
''')

db.exec('''
    CREATE TABLE IF NOT EXISTS workshops (
        wid INTEGER PRIMARY KEY,
        name VARCHAR(20),
        location VARCHAR(40),
        availability VARCHAR(20),
        price_in_hours INTEGER)             
''')
# ----MAKING MANY-TO-MANY RELATIONSHIPS----
db.exec('''
    CREATE TABLE IF NOT EXISTS workshops_have_car_parts (
    wid INTEGER, 
    cpid INTEGER
    )
''')

db.exec('''
    CREATE TABLE IF NOT EXISTS providers_provide_car_parts (
    pid INTEGER, 
    cpid INTEGER
    )
''')

db.exec('''
    CREATE TABLE IF NOT EXISTS cars_have_car_parts (
    carid INTEGER,
    cpid INTEGER
    )
''')

db.exec('''
    CREATE TABLE IF NOT EXISTS charging_stations_suits_plug_types (
    ptid INTEGER, 
    csid INTEGER
    )
''')

del db

