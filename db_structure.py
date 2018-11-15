
from interface import Database
db = Database('db.sqlite')
db.clear_all()

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
    CREATE TABLE IF NOT EXISTS payments (
    payid INTEGER PRIMARY KEY,
    cid INTEGER UNIQUE,
    paytime DATETIME,
    FOREIGN KEY (cid) REFERENCES customers(cid)
    )
''')

db.exec('''
    CREATE TABLE IF NOT EXISTS rides (
        rid INTEGER PRIMARY KEY,
        initial_car_location VARCHAR(40),
        source_location VARCHAR(40),
        destination VARCHAR(40),
        start_ride_time TIMESTAMP,
        end_ride_time TIMESTAMP,
        carid INTEGER, 
        cid INTEGER,
        FOREIGN KEY (carid) REFERENCES cars(carid),
        FOREIGN KEY (cid) REFERENCES customers(cid)
        )
''')

db.exec('''
    CREATE TABLE IF NOT EXISTS cars (
        carid INTEGER PRIMARY KEY,
        plate VARCHAR(20),
        color VARCHAR(20),
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
    CREATE TABLE IF NOT EXISTS car_parts (
        cpid INTEGER PRIMARY KEY, 
        title VARCHAR(40))                   
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
    CREATE TABLE IF NOT EXISTS workshops_sell_car_parts (
    wid INTEGER, 
    cpid INTEGER, 
    selltime DATETIME NULL, 
    amount INTEGER,
    price INTEGER
    )
''')

db.exec('''
    CREATE TABLE IF NOT EXISTS providers_provide_car_parts (
    pid INTEGER, 
    cpid INTEGER
    )
''')

db.exec('''
    CREATE TABLE IF NOT EXISTS cars_repaired (
    carid INTEGER, 
    wid INTEGER,
    price INTEGER
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

db.exec('''
    CREATE TABLE IF NOT EXISTS cars_charged (
    carid INTEGER, 
    csid INTEGER,
    usage_time DATETIME,
    charging_time_amount INTEGER, 
    price INTEGER
    )
''')

del db

