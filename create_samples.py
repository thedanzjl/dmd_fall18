import random
import string
from datetime import datetime
from interface import Database

db = Database("db.sqlite")
db.clear_all()


# INSERTING customers SAMPLES
N = 10

names = ['Daniel', 'Roman', 'Mary', 'Nikolay', 'Nikita', 'Subham', 'Joo', 'Manuel']
locations = ['Universitetskaya 1', 'Sportivnaya 3', 'Sportivnaya 108', 'Kvantovy bulvar 1', 'Centralnaya 5']
locations2 = ['Universitetskaya 1/2', 'Sportivnaya 30', 'Sportivnaya 1', 'Kvantovy bulvar 12', 'Centralnaya 15']


chars = string.printable[:62]
usernames = list()
for _ in range(N):  # generate random usernames
    username = ''
    for i in range(random.randint(5, 10)):
        username += random.choice(chars)
    usernames.append(username)

for id in range(N):
    username = usernames[id]
    full_name = random.choice(names)
    location = random.choice(locations)
    phone_number = ''.join([random.choice('0123456789') for i in range(11)])
    email = username + random.choice(['@mail.ru', '@gmail.com', '@innopolis.ru', '@bk.ru'])

    db.insert_into('customers', cid=id, username=username, full_name=full_name, location=location,
                phone_number=phone_number, email=email)

# INSERTING cars SAMPLES

colors = ['Red', 'Green', 'Blue', 'Black', 'White']
states = ['broken', 'awaiting', 'busy', 'charging']
plates = []
for i in range(N):
    plate = ''
    plate += random.choice('ABCDEFGHIJKLMN')
    plate += random.choice('ABCDEFGHIJKLMN')
    for _ in range(3):
        plate += random.choice('1234567890')
    plates.append(plate)

for id, plate in enumerate(plates):
    color = random.choice(colors)
    current_state = random.choice(states)
    battery_level = ''.join([random.choice('0123456789') for _ in range(2)])
    location = str(random.choice(locations2)) + ''.join([random.choice('0123456789') for _ in range(3)])
    ptid = random.randint(0, N-1)

    db.insert_into('cars', carid=id, plate=plate, color=color, current_state=current_state,
                   battery_level=battery_level, location=location, ptid=ptid)

db.insert_into('cars', carid=len(plates), plate='AN123', color='Red', current_state='busy',
               battery_level=71, location=locations[0], ptid=1)


# INSERTING rides SAMPLES

for _ in range(N):
    initial_location = random.choice(locations)
    source_location = random.choice(locations)
    destination = random.choice(locations)
    start_ride_time = datetime(2018, random.randint(1, 12), random.randint(1, 28), random.randint(0, 1), random.randint(0, 59), 0)
    end_ride_time = datetime(2018, int(start_ride_time.month), int(start_ride_time.day), random.randint(2, 3), random.randint(0, 59), 0)
    carid = random.randint(0, N - 1)
    cid = random.randint(0, N - 1)

    db.insert_into('rides', initial_car_location=initial_location, source_location=source_location,
                   destination=destination, cid=cid, start_ride_time=start_ride_time, end_ride_time=end_ride_time,
                   carid=carid)
db.insert_into('rides', initial_car_location='1', source_location='2',
                     destination='3', cid=1, distance=random.randint(1, 100), start_ride_time=datetime(2018, 10, 5, 2, random.randint(0, 59), 0), end_ride_time=datetime(2018, 10, 5, 3, random.randint(0, 59), 0),
                     carid=7)
db.insert_into('rides', initial_car_location='1', source_location='2',
                     destination='3', cid=1, distance=random.randint(1, 100),start_ride_time=datetime(2018, 10, 6, 2, random.randint(0, 59), 0), end_ride_time=datetime(2018, 10, 6, 3, random.randint(0, 59), 0),
                     carid=9)
db.insert_into('rides', initial_car_location='1', source_location='2',
                     destination='3', cid=1, distance=random.randint(1, 100),start_ride_time=datetime(2018, 10, 7, 2, random.randint(0, 59), 0), end_ride_time=datetime(2018, 10, 7, 3, random.randint(0, 59), 0),
                     carid=10)
db.insert_into('rides', initial_car_location='1', source_location='2',
                     destination='3', cid=2, distance=random.randint(1, 100),start_ride_time=datetime(2018, 10, 6, 2, random.randint(0, 59), 0), end_ride_time=datetime(2018, 10, 6, 3, random.randint(0, 59), 0),
                     carid=10)


# INSERTING cars_charged SAMPLES

for carid in range(N):
    for csid in range(N):
        usage_time = datetime(2018, random.randint(1, 12), random.randint(1, 28), random.randint(0, 12), random.randint(0, 59), 0)
        charging_time_amount = random.randint(10, 60)
        price = random.randint(100, 500)
        db.insert_into('cars_charged', carid=carid, csid=csid, usage_time=usage_time,
                       charging_time_amount=charging_time_amount, price=price)

db.insert_into('cars_charged', carid=7, csid=2, usage_time=datetime(2018, 10, 5, 5, random.randint(0, 59), 0),
                      charging_time_amount=20, price=100)

db.insert_into('cars_charged', carid=9, csid=2, usage_time=datetime(2018, 10, 6, 5, random.randint(0, 59), 0),
                      charging_time_amount=20, price=100)

db.insert_into('cars_charged', carid=9, csid=2, usage_time=datetime(2018, 10, 10, 5, random.randint(0, 59), 0),
                      charging_time_amount=20, price=100)

db.insert_into('cars_charged', carid=10, csid=2, usage_time=datetime(2018, 10, 6, 5, random.randint(0, 59), 0),
                      charging_time_amount=20, price=100)



# INSERTING plug_types SAMPLES

for id in range(N):
    size = random.randint(0, 5)
    shape = random.choice(('square', 'circle', 'rectangle'))

    db.insert_into('plug_types', ptid=id, size=size, shape=shape)


# INSERTING charging_stations SAMPLES

for id in range(N):
    location = random.choice(locations)
    price = random.randint(100, 500)
    amount_of_sockets = random.randint(0, 10)

    db.insert_into('charging_stations', csid=id, location=location, price=price,
                   amount_of_sockets=amount_of_sockets)


# INSERTING car_parts SAMPLES

car_parts = ('steering wheel', 'wheel', 'motor', 'wipers', 'seat', 'door', 'carburetor', 'radio')

for id, title in enumerate(car_parts):
    db.insert_into('car_parts', cpid=id, title=title)


# INSERTING providers SAMPLES

providers = ('SuperCar', 'BestProvider', 'CatAndCar')
for id, name in enumerate(providers):
    phone_number = random.choice(('2550550', '4368993', '4324600'))
    location = random.choice(locations)
    db.insert_into('providers', pid=id, name=name, phone_number=phone_number, location=location)


# INSERTING workshops SAMPLES

workshops = ('BestWorkshop', 'MadeInChina', 'CrazyKuzya')
for id, name in enumerate(workshops):
    location = random.choice(locations)
    db.insert_into('workshops', wid=id, name=name, location=location)


# INSERTING workshops_sell_car_parts SAMPLES

for cpid in range(len(car_parts)):
    for wid in range(len(workshops)):
        if random.randint(0, 1):
            selltime = datetime(2018, 11, 16, random.randint(0, 1), random.randint(0, 59), 0)
        else:
            selltime = None
        amount = random.randint(0, 30)
        price = random.randint(500, 10000)

        db.insert_into('workshops_sell_car_parts', wid=wid, cpid=cpid, selltime=selltime, amount=amount, price=price)


# INSERTING providers_provide_car_parts SAMPLES

for pid in range(N):
    for cpid in range(N):
        if random.randint(0, 3):
            db.insert_into('providers_provide_car_parts', pid=pid, cpid=cpid)


# INSERTING cars_repaired SAMPLES

for carid in range(N):
    for wid in range(len(workshops)):
        price = random.randint(1000, 50000)
        if random.randint(0, 1):
            db.insert_into('cars_repaired', carid=carid, wid=wid, price=price)


# INSERTING cars_have_car_parts SAMPLES

for carid in range(N):
    for cpid in range(N):
        db.insert_into('cars_have_car_parts', carid=carid, cpid=cpid)


# INSERTING charging_stations_suits_plug_types SAMPLES

for csid in range(N):
    ptid = random.randint(0, N-1)
    db.insert_into('charging_stations_suits_plug_types', ptid=ptid, csid=csid)



# INSERTING payments SAMPLES

for payid in range(N):
    cid = random.randint(0, N-1)
    paytime = datetime(2018, random.randint(1, 11), random.randint(1, 10), random.randint(0, 12), random.randint(0, 59), 0)
    amount = random.randint(100, 700)
    db.insert_into('payments', payid=payid, cid=cid, paytime=paytime, amount=amount)

# close database
del db


