
from interface import Database
db = Database('db.sqlite')

# ----CREATING TABLES----

db.exec("PRAGMA foreign_keys=ON")
db.exec('''
    CREATE TABLE customers (
        cid INTEGER PRIMARY KEY,                                 
        username VARCHAR(30) NOT NULL,                                 
        full_name VARCHAR(40),
        location VARCHAR(40),
        phone_number VARCHAR(11),
        email VARCHAR(40)
        )                              
''')

db.exec('''
    CREATE TABLE rides (
        rid INTEGER PRIMARY KEY,
        initial_location VARCHAR(40),
        destination VARCHAR(40),
        cid INTEGER UNIQUE, # one-to-one connection to customer
        FOREIGN KEY (cid) references customers(cid),
        carid INTEGER UNIQUE , # one-to-one connection to car
        FOREIGN KEY (carid) references cars(carid)
        )                            
''')

db.exec('''
    CREATE TABLE cars (
        carid INTEGER PRIMARY KEY,
        current_state VARCHAR(20),
        battery_level INTEGER,
        location VARCHAR(40))                          
''')

db.exec('''
    CREATE TABLE plug_types (
        ptid INTEGER PRIMARY KEY,
        shape VARCHAR(20),
        size INTEGER,
        carid INTEGER,
        FOREIGN KEY (carid) REFERENCES cars(carid)
        )                        
''')

db.exec('''
    CREATE TABLE charging_stations (
        csid INTEGER PRIMARY KEY,
        location VARCHAR(40),
        price INTEGER,
        plug_types VARCHAR(40),
        time_of_charging_min INTEGER,
        amount_of_sockets INTEGER)                     
''')

db.exec('''
    CREATE TABLE car_part_types (
        cpid INTEGER PRIMARY KEY,
        price INTEGER)                   
''')

db.exec('''
    CREATE TABLE providers (
        pid INTEGER PRIMARY KEY,
        name VARCHAR(20) NOT NULL,
        phone_number VARCHAR(11),
        location VARCHAR(40)
        )                
''')

db.exec('''
    CREATE TABLE workshops (
        wid INTEGER PRIMARY KEY,
        name VARCHAR(20),
        location VARCHAR(40),
        availability VARCHAR(20),
        price_in_hours INTEGER)             
''')
# ----MAKING MANY-TO-MANY RELATIONSHIPS----
db.exec('''
    CREATE TABLE workshops_have_car_parts (
    wid INTEGER, 
    cpid INTEGER
    )
''')

db.exec('''
    CREATE TABLE providers_provide_car_parts (
    pid INTEGER, 
    cpid INTEGER
    )
''')

db.exec('''
    CREATE TABLE cars_have_car_parts (
    carid INTEGER, 
    cpid INTEGER
    )
''')

db.exec('''
    CREATE TABLE charging_stations_suits_plug_types (
    ptid INTEGER, 
    csid INTEGER
    )
''')

del db

