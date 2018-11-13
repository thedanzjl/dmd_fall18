import random
import string
from interface import Database

db = Database("db.sqlite")
db.clear_all()


# INSERTING CUSTOMER'S SAMPLES
N = 10

names = ['Daniel', 'Roman', 'Mary', 'Nikolay', 'Vladimir']
locations = ['Barbara street 1337', 'Universitetskaya 1', 'Sportivnaya 3']

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

# INSERTING CARS SAMPLES


colors = ['Red', 'Green', 'Blue', 'Black', 'White']
locations2 = ['Barbara street', 'Universitetskaya', 'Sportivnaya']
states = ['broken','awaiting','busy','charging']

for id in range(N):
    plate = ''.join([random.choice('0123456789') for i in range(5)])
    color = random.choice(colors)
    current_state = random.choice(states)
    battery_level = ''.join([random.choice('0123456789') for i in range(2)])
    location = str(random.choice(locations2)) + ''.join([random.choice('0123456789') for i in range(3)])
    ptid = ''.join([random.choice('0123456789') for i in range(2)])

    db.insert_into('cars', carid=id, plate=plate, color=color, current_state=current_state,
                   battery_level = battery_level, location = location, ptid = ptid)


# INSERTING RIDES SAMPLES

# INSERTING PLUG_TYPES SAMPLES

# INSERTING CHARGING_STATIONS SAMPLES

# INSERTING CAR_PARTS SAMPLES

# INSERTING PROVIDERS SAMPLES

# INSERTING WORKSHOPS SAMPLES


del db

#
# if __name__ == '__main__':
#     print(db.query("""
#     SELECT * FROM customers
#     """))

