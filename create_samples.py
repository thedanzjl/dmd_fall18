import random
import string
from datetime import datetime
from interface import Database

db = Database("db.sqlite")
db.clear_all()


# INSERTING customers SAMPLES
N = 10

names = ['Daniel', 'Roman', 'Mary', 'Nikolay', 'Vladimir']
locations = ['Barbara street 1337', 'Universitetskaya 1', 'Sportivnaya 3']
locations2 = ['Barbara street', 'Universitetskaya', 'Sportivnaya']


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
    carid = random.randint(0, N-1)
    cid = random.randint(0, N-1)

    db.insert_into('rides', rid=id, initial_car_location=initial_location,
                   source_location=source_location, destination=destination, cid=cid,
                   start_ride_time=start_ride_time, end_ride_time=end_ride_time, carid=carid
                   )

# INSERTING plug_types SAMPLES

# INSERTING charging_stations SAMPLES

# INSERTING car_parts SAMPLES

# INSERTING providers SAMPLES

# INSERTING workshops_sell_car_parts SAMPLES

# INSERTING providers_provide_car_parts SAMPLES

# INSERTING cars_repaired SAMPLES

# INSERTING cars_have_car_parts SAMPLES

# INSERTING charging_stations_suits_plug_types SAMPLES

# INSERTING cars_charged SAMPLES


del db


