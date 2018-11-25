
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
    cid INTEGER,
    paytime DATETIME,
    amount INTEGER, 
    FOREIGN KEY (cid) REFERENCES customers(cid)
    )
''')

db.exec('''
    CREATE TABLE IF NOT EXISTS rides (
        initial_car_location VARCHAR(40),
        source_location VARCHAR(40),
        destination VARCHAR(40),
        start_ride_time DATETIME,
        end_ride_time TIMESTAMP,
        carid INTEGER, 
        cid INTEGER,
        distance INTEGER,
        FOREIGN KEY (carid) REFERENCES cars(carid),
        FOREIGN KEY (cid) REFERENCES customers(cid),
        PRIMARY KEY (carid, cid, start_ride_time)
        )
''')

db.exec('''
    CREATE TABLE IF NOT EXISTS cars (
        carid INTEGER PRIMARY KEY,
        plate VARCHAR(20) UNIQUE,
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
        location VARCHAR(40)
        )             
''')


# ----MAKING MANY-TO-MANY RELATIONSHIPS----
db.exec('''
    CREATE TABLE IF NOT EXISTS workshops_sell_car_parts (
    wid INTEGER, 
    cpid INTEGER, 
    selltime DATETIME NULL, 
    amount INTEGER,
    price INTEGER,
    PRIMARY KEY (wid, cpid), 
    FOREIGN KEY (wid) REFERENCES workshops(wid),
    FOREIGN KEY (cpid) REFERENCES car_part_types(cpid)
    )
''')

db.exec('''
    CREATE TABLE IF NOT EXISTS providers_provide_car_parts (
    pid INTEGER, 
    cpid INTEGER, 
    PRIMARY KEY (pid, cpid), 
    FOREIGN KEY (pid) REFERENCES providers(pid),
    FOREIGN KEY (cpid) REFERENCES car_part_types(cpid)
    )
''')

db.exec('''
    CREATE TABLE IF NOT EXISTS cars_repaired (
    carid INTEGER, 
    wid INTEGER,
    price INTEGER, 
    PRIMARY KEY (carid, wid), 
    FOREIGN KEY (carid) REFERENCES cars(carid),
    FOREIGN KEY (wid) REFERENCES workshops(wid)
    )
''')

db.exec('''
    CREATE TABLE IF NOT EXISTS cars_have_car_parts (
    carid INTEGER,
    cpid INTEGER, 
    PRIMARY KEY (carid, cpid), 
    FOREIGN KEY (carid) REFERENCES cars(carid),
    FOREIGN KEY (cpid) REFERENCES car_part_types(cpid)
    )
''')

db.exec('''
    CREATE TABLE IF NOT EXISTS charging_stations_suits_plug_types (
    ptid INTEGER, 
    csid INTEGER, 
    PRIMARY KEY (ptid, csid), 
    FOREIGN KEY (ptid) REFERENCES plug_types(ptid),
    FOREIGN KEY (csid) REFERENCES charging_stations(csid)
    )
''')

db.exec('''
    CREATE TABLE IF NOT EXISTS cars_charged (
    carid INTEGER, 
    csid INTEGER,
    usage_time DATETIME,
    charging_time_amount INTEGER, 
    price INTEGER, 
    PRIMARY KEY (carid, csid, usage_time), 
    FOREIGN KEY (carid) REFERENCES cars(carid),
    FOREIGN KEY (csid) REFERENCES charging_stations(csid)
    )
''')

del db

