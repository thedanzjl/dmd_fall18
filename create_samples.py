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
states = ['broken','awaiting','busy','charging']

for id in range(N):
    plate = ''.join([random.choice('0123456789') for _ in range(5)])
    color = random.choice(colors)
    current_state = random.choice(states)
    battery_level = ''.join([random.choice('0123456789') for _ in range(2)])
    location = str(random.choice(locations2)) + ''.join([random.choice('0123456789') for _ in range(3)])
    ptid = ''.join([random.choice('0123456789') for i in range(2)])

    db.insert_into('cars', carid=id, plate=plate, color=color, current_state=current_state,
                   battery_level=battery_level, location=location, ptid=ptid)


# INSERTING rides SAMPLES

for id in range(N):
    initial_location = random.choice(locations)
    source_location = random.choice(locations)
    destination = random.choice(locations)
    start_ride_time = datetime(2018, 11, 16, random.randint(0, 1), random.randint(0, 59), 0)
    end_ride_time = datetime(2018, 11, 16, random.randint(2, 3), random.randint(0, 59), 0)
    carid = random.randint(0, N - 1)
    cid = random.randint(0, N - 1)

    db.insert_into('rides', rid=id, initial_car_location=initial_location, source_location=source_location,
                   destination=destination, cid=cid, start_ride_time=start_ride_time, end_ride_time=end_ride_time,
                   carid=carid)


# INSERTING plug_types SAMPLES

for id in range(N):
    size = random.randint(0, 5)
    shape = random.choice('square', 'circle', 'rectangle')

    db.insert_into('plug_types', ptid=id, size=size, shape=shape)


# INSERTING charging_stations SAMPLES

for id in range(N):
    location = random.choice(locations)
    price = random.randint(100, 500)
    plug_types = random.choice('square', 'circle', 'rectangle')
    time_of_charging_min = random.randint(10, 60)
    amount_of_sockets = random.randint(0, 10)

    db.insert_into('charging_stations', csid=id, location=location, price=price, plug_types=plug_types,
                   time_of_charging_min=time_of_charging_min, amount_of_sockets=amount_of_sockets)


# INSERTING car_parts SAMPLES

for id in range(N):
    title = random.choice('steering wheel', 'wheel', 'motor', 'wipers', 'seat', 'door', 'carburetor', 'radio')

    db.insert_into('car_parts', cpid=id, title=title)

# INSERTING providers SAMPLES

for id in range(N):
    name = random.choice('SuperCar', 'BestProvider', 'CatAndCar')
    phone_number = ('2550550', '4368993', '4324600')
    location = random.choice(locations)

    db.insert_into('providers', pid=id, name=name, phone_number=phone_number, location=location)


# INSERTING workshops_sell_car_parts SAMPLES

for id in range(N):
    wid = random.randint(0, N - 1)
    cpid = random.randint(0, N - 1)
    selltime = datetime(2018, 11, 16, random.randint(0, 1), random.randint(0, 59), 0)
    amount = random.randint(0, 100)
    price = random.randint(500, 10000)

    db.insert_into('workshops_sell_car_parts', wid=wid, cpid=cpid, selltime=selltime, amount=amount, price=price)


# INSERTING providers_provide_car_parts SAMPLES

for id in range(N):
    pid = random.randint(0, N - 1)
    cpid = random.randint(0, N - 1)

    db.insert_into('providers_provide_car_parts', pid=pid, cpid=cpid)


# INSERTING cars_repaired SAMPLES

for id in range(N):
    carid = random.randint(0, N - 1)
    wid = random.randint(0, N - 1)
    price = random.randint(0, N - 1)

    db.insert_into('cars_rapaired', carid=carid, wid=wid, price=price)


# INSERTING cars_have_car_parts SAMPLES

for i in range(N):
    carid = random.randint(0, N - 1)
    cpid = random.randint(0, N - 1)

    db.insert_into('cars_have_car_parts', carid=carid, cpid=cpid)


# INSERTING charging_stations_suits_plug_types SAMPLES

for i in range(N):
    ptid = random.randint(0, N - 1)
    csid = random.randint(0, N - 1)

    db.insert_into('charging_stations_suits_plug_types', ptid=ptid, csid=csid)


# INSERTING cars_charged SAMPLES

for i in range(N):
    carid = random.randint(0, N - 1)
    csid = random.randint(0, N - 1)
    usage_time = datetime(2018, 11, 16, random.randint(0, 1), random.randint(0, 59), 0)
    charging_time_amount = random.randint(10, 60)
    price = random.randint(100, 500)

    db.insert_into('cars_charged', carid=carid, csid=csid, usage_time=usage_time,
                   charging_time_amount=charging_time_amount, price=price)

del db


